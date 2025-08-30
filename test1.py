#!/usr/bin/env python3
"""
md_block_diff_from_matches.py — derive differences from block indexes + matches.

Inputs:
  - LEFT index JSONL  (from `md_block_match.py index ... > old.jsonl`)
  - RIGHT index JSONL (from `md_block_match.py index ... > new.jsonl`)
  - MATCHES JSONL     (from `md_block_match.py match old.jsonl new.jsonl > matches.jsonl`)

Output:
  JSONL of difference records to stdout. Logs/progress go to stderr.

Record shapes:
  {"change":"added", "right": {...}}
  {"change":"removed", "left": {...}}
  {"change":"moved", "left": {...}, "right": {...}}
  {"change":"modified", "left": {...}, "right": {...}, "hamming": 7, "sim": 0.890625}
  {"change":"moved_modified", ...}
  {"change":"split", "left": {...}, "rights": [{...}, {...}]}
  {"change":"merged","right": {...}, "lefts": [{...}, {...}]}
  (optional) {"change":"unchanged", "left": {...}, "right": {...}}

Notes:
  - “location changed” = file path OR section_path differ.
  - Splits/merges are heuristic: they report when multiple candidates exist.
  - Deterministic: for each left, we pick the best match (prefer exact; else min hamming; ties by lexicographic right_id).
"""
from __future__ import annotations
import argparse, json, sys
from typing import Dict, List, Tuple, Iterable, Any, Optional

def eprint(*a, **k): print(*a, file=sys.stderr, **k)

def load_jsonl(path: str) -> Iterable[dict]:
    f = sys.stdin if path == "-" else open(path, "r", encoding="utf-8")
    with f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as ex:
                    eprint(f"[jsonl] bad line: {ex}: {line[:120]}")

def block_id(rec: dict) -> str:
    return f'{rec["repo"]}|{rec["file"]}|{rec["block_ix"]}'

def same_location(a: dict, b: dict) -> bool:
    return (a["file"] == b["file"]) and (a.get("section_path", []) == b.get("section_path", []))

def pick_best_matches(matches: Iterable[dict]) -> Tuple[Dict[str, dict], Dict[str, dict], Dict[str, List[dict]], Dict[str, List[dict]]]:
    """
    Returns:
      best_by_left  : left_id -> best match object
      best_by_right : right_id -> best match object
      all_by_left   : left_id -> list of all match objects (duplicates kept)
      all_by_right  : right_id -> list of all match objects
    """
    all_by_left: Dict[str, List[dict]] = {}
    all_by_right: Dict[str, List[dict]] = {}
    for m in matches:
        lid, rid = m["left_id"], m["right_id"]
        all_by_left.setdefault(lid, []).append(m)
        all_by_right.setdefault(rid, []).append(m)

    def best(ms: List[dict]) -> dict:
        # Prefer exact (hamming==0). Otherwise min hamming; break ties by right_id for determinism.
        exact = [m for m in ms if m.get("score_equal")]
        if exact:
            # If multiple exact, pick lexicographically smallest right_id
            return sorted(exact, key=lambda x: x["right_id"])[0]
        return sorted(ms, key=lambda x: (x.get("hamming", 999), x["right_id"]))[0]

    best_by_left = {lid: best(ms) for lid, ms in all_by_left.items()}
    # One right can have multiple left candidates; also pick best per right (symmetrically)
    def best_r(ms: List[dict]) -> dict:
        exact = [m for m in ms if m.get("score_equal")]
        if exact:
            return sorted(exact, key=lambda x: x["left_id"])[0]
        return sorted(ms, key=lambda x: (x.get("hamming", 999), x["left_id"]))[0]
    best_by_right = {rid: best_r(ms) for rid, ms in all_by_right.items()}

    return best_by_left, best_by_right, all_by_left, all_by_right

def classify_diffs(
    left_index: List[dict],
    right_index: List[dict],
    best_by_left: Dict[str, dict],
    best_by_right: Dict[str, dict],
    all_by_left: Dict[str, List[dict]],
    all_by_right: Dict[str, List[dict]],
    include_unchanged: bool,
) -> Iterable[dict]:
    left_map: Dict[str, dict] = {block_id(r): r for r in left_index}
    right_map: Dict[str, dict] = {block_id(r): r for r in right_index}
    left_ids = set(left_map.keys())
    right_ids = set(right_map.keys())

    matched_left = set(best_by_left.keys())
    matched_right = set(best_by_right.keys())

    # Removed / Added
    for lid in sorted(left_ids - matched_left):
        yield {"change": "removed", "left": left_map[lid]}
    for rid in sorted(right_ids - matched_right):
        yield {"change": "added", "right": right_map[rid]}

    # Matched (differences & optional unchanged)
    for lid in sorted(matched_left):
        m = best_by_left[lid]
        l = m["left"]; r = m["right"]
        # Sanity: left/right in maps? (they should be)
        lrec = l if isinstance(l, dict) else left_map.get(lid)
        rrec = r if isinstance(r, dict) else right_map.get(m["right_id"])
        if not (lrec and rrec):
            continue

        if m.get("score_equal"):
            if same_location(lrec, rrec):
                if include_unchanged:
                    yield {"change": "unchanged", "left": lrec, "right": rrec}
            else:
                yield {"change": "moved", "left": lrec, "right": rrec}
        else:
            loc_same = same_location(lrec, rrec)
            base = {
                "left": lrec,
                "right": rrec,
                "hamming": m.get("hamming"),
                "sim": m.get("sim"),
            }
            if loc_same:
                yield {"change": "modified", **base}
            else:
                yield {"change": "moved_modified", **base}

    # Heuristics: split / merged
    for lid, ms in sorted(all_by_left.items()):
        if len(ms) >= 2:
            rights = [m["right"] for m in sorted(ms, key=lambda x: (x.get("hamming", 999), x["right_id"]))[:4]]
            yield {"change": "split", "left": ms[0]["left"], "rights": rights}
    for rid, ms in sorted(all_by_right.items()):
        if len(ms) >= 2:
            lefts = [m["left"] for m in sorted(ms, key=lambda x: (x.get("hamming", 999), x["left_id"]))[:4]]
            yield {"change": "merged", "right": ms[0]["right"], "lefts": lefts}

def report_tsv(diffs: Iterable[dict]) -> str:
    counts: Dict[str, int] = {}
    for d in diffs:
        counts[d["change"]] = counts.get(d["change"], 0) + 1
    lines = ["change\tcount"]
    for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"{k}\t{v}")
    return "\n".join(lines) + "\n"

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Derive differences from block indexes + matches JSONL.")
    ap.add_argument("left", help="Left index JSONL (or '-' for stdin)")
    ap.add_argument("right", help="Right index JSONL")
    ap.add_argument("matches", help="Matches JSONL")
    ap.add_argument("--include-unchanged", action="store_true", help="Also emit unchanged records")
    ap.add_argument("--report", action="store_true", help="Print a TSV summary instead of JSONL")
    args = ap.parse_args(argv)

    left = list(load_jsonl(args.left))
    right = list(load_jsonl(args.right))
    matches = list(load_jsonl(args.matches))
    eprint(f"[diff] left blocks: {len(left)}; right blocks: {len(right)}; matches: {len(matches)}")

    best_l, best_r, all_l, all_r = pick_best_matches(matches)
    diffs_iter = list(classify_diffs(left, right, best_l, best_r, all_l, all_r, args.include_unchanged))

    if args.report:
        sys.stdout.write(report_tsv(diffs_iter))
    else:
        for d in diffs_iter:
            sys.stdout.write(json.dumps(d, ensure_ascii=False) + "\n")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
