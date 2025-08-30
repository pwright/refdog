#!/usr/bin/env python3
"""
md_block_match.py — Block-level matching for refactored Markdown trees.

Subcommands:
  index  : produce a JSONL index of blocks from a directory or a file list
  match  : consume two JSONL indexes and emit block-to-block matches (JSONL)
  report : summarize matches (TSV)

JSONL (index) fields per line:
  {
    "repo": "<label or root path>",
    "file": "relative/or/absolute.md",
    "section_path": ["Top heading", "Subheading", ...],
    "block_ix": 0,
    "kind": "paragraph|code|table|list|heading",
    "sha1": "<40-hex>",
    "simhash": "<16-hex-64bit>",
    "tokens": 123,
    "chars": 456,
    "heading_level": 1,               # for 'heading' kind
    "text": "original block text..."
  }

JSONL (match) fields:
  {
    "left_id": "<repo>|<file>|<block_ix>",
    "right_id": "<repo>|<file>|<block_ix>",
    "score_equal": true|false,
    "hamming": 7,
    "sim": 0.890625,                  # 1 - hamming/64
    "left": { ...index object... },
    "right": { ...index object... }
  }

Notes:
- Accepts stdin ('-') with optional --nul to handle NUL-delimited file lists.
- All outputs go to stdout; diagnostics to stderr.
- No third-party dependencies; pure Python 3.8+.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Tuple, Dict, Any, Optional, Sequence

##############
# Utilities  #
##############

def eprint(*a, **k):
    print(*a, file=sys.stderr, **k)

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def sha1_hex(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", "ignore")).hexdigest()

def strip_front_matter(s: str) -> str:
    # Remove leading '--- ... ---' front matter
    if s.startswith("---\n"):
        end = s.find("\n---", 4)
        if end != -1:
            after = s[end+4:]
            # Drop following blank lines
            return re.sub(r"^\s*\n", "", after, count=1, flags=re.MULTILINE)
    return s

def normalize_inline(md: str) -> str:
    """Lightweight Markdown inline normalization for similarity:
    - remove emphasis markers * _ ~
    - replace links [text](url) -> 'text url'
    - strip backticks around inline code
    - collapse whitespace, lowercase
    """
    s = md
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 \2", s)
    s = re.sub(r"[*_~]+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.lower()

def tokenize(s: str) -> List[str]:
    # Words and numbers; keep URLs host/path chunks together as best effort
    return re.findall(r"[A-Za-z0-9_/.\-]+", s)

def word_shingles(tokens: Sequence[str], k: int = 3) -> Iterator[str]:
    if k <= 1 or len(tokens) < k:
        for t in tokens:
            yield t
        return
    for i in range(len(tokens) - k + 1):
        yield " ".join(tokens[i:i+k])

def simhash64(tokens: Iterable[str]) -> int:
    """64-bit SimHash over tokens."""
    v = [0] * 64
    for tok in tokens:
        h = int(hashlib.blake2b(tok.encode("utf-8"), digest_size=8).hexdigest(), 16)
        for bit in range(64):
            v[bit] += 1 if (h >> bit) & 1 else -1
    out = 0
    for bit in range(64):
        if v[bit] >= 0:
            out |= (1 << bit)
    return out

def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()

#########################
# Markdown block split  #
#########################

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE_RE = re.compile(r"^(```|~~~)")

@dataclass
class Block:
    kind: str                 # paragraph|code|table|list|heading
    text: str
    section_path: List[str]
    heading_level: Optional[int] = None

def split_blocks(md: str) -> List[Block]:
    """Segment Markdown into semantic blocks under a running section_path."""
    md = strip_front_matter(md)
    lines = md.splitlines()
    blocks: List[Block] = []
    buf: List[str] = []
    buf_kind: Optional[str] = None
    section_path: List[str] = []
    i = 0
    in_code = False
    code_fence = None

    def flush_paragraph():
        nonlocal buf, buf_kind
        if buf:
            text = "\n".join(buf).strip("\n")
            if text.strip():
                blocks.append(Block(kind=buf_kind or "paragraph", text=text, section_path=section_path.copy()))
        buf = []
        buf_kind = None

    while i < len(lines):
        line = lines[i]

        # Headings
        m = HEADING_RE.match(line)
        if not in_code and m:
            flush_paragraph()
            level = len(m.group(1))
            title = m.group(2).strip()
            # update section path
            if level <= len(section_path):
                section_path = section_path[:level-1]
            while len(section_path) < level-1:
                section_path.append("")  # pad if malformed
            section_path = section_path[:level-1] + [title]
            blocks.append(Block(kind="heading", text=title, section_path=section_path.copy(), heading_level=level))
            i += 1
            continue

        # Fenced code
        if not in_code and FENCE_RE.match(line.strip()):
            flush_paragraph()
            in_code = True
            code_fence = line.strip()[:3]
            buf_kind = "code"
            buf = [line]
            i += 1
            continue
        if in_code:
            buf.append(line)
            if FENCE_RE.match(line.strip()):
                # try to detect closing fence
                if line.strip().startswith(code_fence):
                    blocks.append(Block(kind="code", text="\n".join(buf), section_path=section_path.copy()))
                    buf, buf_kind = [], None
                    in_code = False
                    code_fence = None
            i += 1
            continue

        # Tables (lines containing pipes) – accumulate until blank line
        if "|" in line and re.search(r"\S\|\S", line):
            if buf_kind not in (None, "table"):
                flush_paragraph()
            buf_kind = "table"
            buf.append(line)
            # Lookahead to see if table continues
            j = i + 1
            while j < len(lines) and ("|" in lines[j] or re.match(r"^\s*:-", lines[j])):
                buf.append(lines[j])
                j += 1
            blocks.append(Block(kind="table", text="\n".join(buf), section_path=section_path.copy()))
            buf, buf_kind = [], None
            i = j
            continue

        # Lists – simple heuristic: lines starting with -,*,+ or numbered
        if re.match(r"^\s*([-*+]|[0-9]+\.)\s+", line):
            if buf_kind not in (None, "list"):
                flush_paragraph()
            buf_kind = "list"
            buf.append(line)
            # absorb contiguous list lines
            j = i + 1
            while j < len(lines) and (re.match(r"^\s{0,4}([-*+]|[0-9]+\.)\s+", lines[j]) or lines[j].strip() == "" or lines[j].startswith("  ")):
                buf.append(lines[j])
                j += 1
            blocks.append(Block(kind="list", text="\n".join(buf), section_path=section_path.copy()))
            buf, buf_kind = [], None
            i = j
            continue

        # Blank line flushes paragraph
        if line.strip() == "":
            flush_paragraph()
            i += 1
            continue

        # Paragraph
        if buf_kind not in (None, "paragraph"):
            flush_paragraph()
        buf_kind = "paragraph"
        buf.append(line)
        i += 1

    # tail
    if in_code:
        blocks.append(Block(kind="code", text="\n".join(buf), section_path=section_path.copy()))
    else:
        flush_paragraph()

    return blocks

#############################
# Indexing & Matching I/O   #
#############################

def index_stream(paths: Iterable[str], repo_label: str) -> Iterator[Dict[str, Any]]:
    for p in paths:
        if not p:
            continue
        p = os.path.abspath(p)
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fn in files:
                    if fn.lower().endswith(".md"):
                        yield from index_file(os.path.join(root, fn), repo_label)
        else:
            if p.lower().endswith(".md"):
                yield from index_file(p, repo_label)

def index_file(path: str, repo_label: str) -> Iterator[Dict[str, Any]]:
    try:
        txt = read_text(path)
    except Exception as ex:
        eprint(f"[index] failed to read {path}: {ex}")
        return
    blocks = split_blocks(txt)
    for ix, b in enumerate(blocks):
        norm = normalize_inline(b.text)
        toks = tokenize(norm)
        shingles = list(word_shingles(toks, k=3))
        sh = simhash64(shingles if shingles else toks)
        rec = {
            "repo": repo_label,
            "file": path,
            "section_path": b.section_path,
            "block_ix": ix,
            "kind": b.kind,
            "sha1": sha1_hex(norm),
            "simhash": f"{sh:016x}",
            "tokens": len(toks),
            "chars": len(norm),
        }
        if b.kind == "heading":
            rec["heading_level"] = b.heading_level
        rec["text"] = b.text
        yield rec

def load_jsonl(fp: io.TextIOBase) -> Iterator[Dict[str, Any]]:
    for line in fp:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError as ex:
            eprint(f"[jsonl] bad line: {ex}: {line[:120]}")

def match_indexes(
    left: Iterable[Dict[str, Any]],
    right: Iterable[Dict[str, Any]],
    hamming_max: int = 8,
    use_lsh: bool = True,
    lsh_bits: int = 16,
) -> Iterator[Dict[str, Any]]:
    # Build maps for right side
    right_by_sha: Dict[str, List[Dict[str, Any]]] = {}
    right_by_bucket: Dict[str, List[Dict[str, Any]]] = {}

    def bucket(simhex: str) -> str:
        # take high lsh_bits
        val = int(simhex, 16)
        mask = ((1 << lsh_bits) - 1) << (64 - lsh_bits)
        return f"{(val & mask) >> (64 - lsh_bits):0{(lsh_bits+3)//4}x}"

    right_list = list(right)
    for r in right_list:
        right_by_sha.setdefault(r["sha1"], []).append(r)
        if use_lsh:
            b = bucket(r["simhash"])
            right_by_bucket.setdefault(b, []).append(r)

    for l in left:
        lid = f'{l["repo"]}|{l["file"]}|{l["block_ix"]}'
        candidates: List[Dict[str, Any]] = []
        # exact
        if l["sha1"] in right_by_sha:
            for r in right_by_sha[l["sha1"]]:
                rid = f'{r["repo"]}|{r["file"]}|{r["block_ix"]}'
                yield {
                    "left_id": lid,
                    "right_id": rid,
                    "score_equal": True,
                    "hamming": 0,
                    "sim": 1.0,
                    "left": l,
                    "right": r,
                }
            continue

        # near: LSH bucket or full scan fallback
        if use_lsh:
            b = bucket(l["simhash"])
            candidates = right_by_bucket.get(b, [])
        else:
            candidates = right_list

        lsim = int(l["simhash"], 16)
        best: Tuple[int, Optional[Dict[str, Any]]] = (65, None)
        for r in candidates:
            rsim = int(r["simhash"], 16)
            d = hamming(lsim, rsim)
            if d < best[0]:
                best = (d, r)

        if best[1] is not None and best[0] <= hamming_max:
            r = best[1]
            rid = f'{r["repo"]}|{r["file"]}|{r["block_ix"]}'
            yield {
                "left_id": lid,
                "right_id": rid,
                "score_equal": False,
                "hamming": best[0],
                "sim": 1.0 - best[0] / 64.0,
                "left": l,
                "right": r,
            }

############
# CLI      #
############

def cmd_index(args: argparse.Namespace) -> int:
    repo = args.label or (args.path if args.path != "-" else "(stdin)")
    if args.path == "-":
        data = sys.stdin.buffer.read()
        paths = data.split(b"\x00") if args.nul else data.splitlines()
        def decode(b): 
            return b.decode("utf-8", "replace").rstrip("\n\r")
        it = (decode(p) for p in paths if p)
    else:
        it = [args.path]
    for rec in index_stream(it, repo_label=repo):
        print(json.dumps(rec, ensure_ascii=False))
    return 0

def cmd_match(args: argparse.Namespace) -> int:
    with open(args.left, "r", encoding="utf-8") as lf, open(args.right, "r", encoding="utf-8") as rf:
        left = list(load_jsonl(lf))
        right = list(load_jsonl(rf))
    eprint(f"[match] left blocks: {len(left)}; right blocks: {len(right)}")
    for m in match_indexes(
        left, right,
        hamming_max=args.hamming_max,
        use_lsh=not args.no_lsh,
        lsh_bits=args.lsh_bits,
    ):
        print(json.dumps(m, ensure_ascii=False))
    return 0

def cmd_report(args: argparse.Namespace) -> int:
    total = 0
    exact = 0
    near = 0
    per_file: Dict[str, Dict[str, int]] = {}
    with (sys.stdin if args.matches == "-" else open(args.matches, "r", encoding="utf-8")) as f:
        for obj in load_jsonl(f):
            total += 1
            if obj.get("score_equal"):
                exact += 1
            else:
                near += 1
            lfile = obj["left"]["file"]
            per_file.setdefault(lfile, {"matches": 0})
            per_file[lfile]["matches"] += 1
    # TSV summary
    print("metric\tcount")
    print(f"total_matches\t{total}")
    print(f"exact_matches\t{exact}")
    print(f"near_matches\t{near}")
    print("\nfile\tmatches")
    for f, s in sorted(per_file.items(), key=lambda kv: (-kv[1]["matches"], kv[0])):
        print(f"{f}\t{s['matches']}")
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="md_block_match.py", description="Block-level matcher for Markdown trees.")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("index", help="Index a directory or a file-list (stdin)")
    pi.add_argument("path", help="Path to dir/file; or '-' to read file list from stdin")
    pi.add_argument("--label", help="Repository/label name for this index (defaults to path or '(stdin)')")
    pi.add_argument("--nul", action="store_true", help="When reading from stdin, expect NUL-delimited records")
    pi.set_defaults(func=cmd_index)

    pm = sub.add_parser("match", help="Match two JSONL indexes")
    pm.add_argument("left", help="Left JSONL index file")
    pm.add_argument("right", help="Right JSONL index file")
    pm.add_argument("--hamming-max", type=int, default=8, help="Max Hamming distance to accept (default 8)")
    pm.add_argument("--no-lsh", action="store_true", help="Disable LSH bucketing (slower, exhaustive)")
    pm.add_argument("--lsh-bits", type=int, default=16, help="High-bit prefix length for buckets (default 16)")
    pm.set_defaults(func=cmd_match)

    pr = sub.add_parser("report", help="Summarize matches (reads matches JSONL)")
    pr.add_argument("matches", help="Path to matches JSONL or '-' for stdin")
    pr.set_defaults(func=cmd_report)

    return p

def main(argv: Optional[List[str]] = None) -> int:
    try:
        parser = build_parser()
        args = parser.parse_args(argv)
        return args.func(args)
    except BrokenPipeError:
        # Allow piping into head/cut without stack traces
        return 0

if __name__ == "__main__":
    sys.exit(main())
