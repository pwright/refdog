# Simple Implementation Plan: CLI Commands Only

**Goal**: Replace current YAML-based command docs with cli-doc + metadata in the simplest way possible.

**Strategy**: Make minimal changes, test with ONE command, then expand.

---

## Why CLI Commands First?

1. **Simpler** - No CRD schema parsing, just markdown
2. **Parser exists** - `python/cli_parser.py` already works
3. **Metadata ready** - 30 files already extracted and validated
4. **Faster proof** - Can see results in 1-2 hours

---

## Current System (What We're Replacing)

```
config/commands/*.yaml  →  python/commands.py  →  input/commands/*.md
     (everything)            (generation)            (output)
```

**Problem**: YAML has everything (descriptions, options, examples). Gets out of sync with actual CLI.

---

## New System (What We're Building)

```
cli-doc/*.md (CLI truth)  ─┐
                           ├─→  python/commands.py  →  input/commands/*.md
metadata/*.yaml (extras)  ─┘     (merge + generate)       (output)
```

**Better**: cli-doc is authoritative for CLI facts, metadata adds documentation enhancements.

---

## The Simplest Possible Implementation

### Phase 1: Add cli-doc Loading (30 minutes)

**File**: `python/commands.py`

**Change 1**: Add import at top
```python
from cli_parser import parse_all_cli_docs
```

**Change 2**: Add to `CommandModel.__init__` (after line 227)
```python
class CommandModel(Model):
    def __init__(self):
        super().__init__(Command, "config/commands")
        
        self.option_data = read_yaml(join(self.config_dir, "options.yaml"))
        
        # NEW: Load cli-doc markdown files
        self.cli_docs = {}
        cli_doc_dir = "cli-doc"
        if exists(cli_doc_dir):
            notice("Loading cli-doc files...")
            self.cli_docs = parse_all_cli_docs(cli_doc_dir)
            notice(f"Loaded {len(self.cli_docs)} cli-doc files")
        
        # Continue with existing code...
        self.init(exclude=["options.yaml", "overview.md", "metadata"])
```

**That's it for Phase 1**. Just load the cli-doc files into memory.

---

### Phase 2: Use cli-doc Data (1 hour)

**File**: `python/commands.py`

**Change**: Modify `Command.__init__` to prefer cli-doc data

**Current logic** (simplified):
```python
class Command:
    def __init__(self, model, data):
        self.description = data.get("description")
        self.options = merge_options_from_yaml()
```

**New logic**:
```python
class Command:
    def __init__(self, model, data):
        # Try to get cli-doc data for this command
        cli_doc = self._get_cli_doc_data()
        
        # Use cli-doc description if available, else YAML
        if cli_doc and cli_doc.get("synopsis"):
            self.description = cli_doc["synopsis"]
        else:
            self.description = data.get("description")
        
        # Use cli-doc options if available, else YAML
        if cli_doc and cli_doc.get("options"):
            self.options = cli_doc["options"]
        else:
            self.options = merge_options_from_yaml()
```

**Add helper method**:
```python
def _get_cli_doc_data(self):
    """Get cli-doc data for this command."""
    # Build command path: "site create"
    parts = [self.name]
    if self.parent:
        parts.insert(0, self.parent.name)
    command_path = " ".join(parts)
    
    # Look it up
    return self.model.cli_docs.get(command_path)
```

**That's it for Phase 2**. Now commands use cli-doc when available.

---

### Phase 3: Test with ONE Command (30 minutes)

```bash
# Generate just one command
./plano generate

# Check the output for "site create"
cat input/commands/site/create.md

# Compare with old version
git diff input/commands/site/create.md
```

**Questions to answer**:
1. Does it generate without errors?
2. Is the description from cli-doc?
3. Are options from cli-doc?
4. Does it look reasonable?

**If yes**: Continue to Phase 4  
**If no**: Fix issues, repeat

---

### Phase 4: Add Metadata Enhancements (1 hour)

Now layer on the metadata (examples, links, etc.)

**File**: `python/commands.py`

**Change**: In `Command.__init__`, after getting cli-doc data:

```python
# After getting cli-doc data...
cli_doc = self._get_cli_doc_data()
metadata = self._get_metadata()

# Start with cli-doc description
if cli_doc and cli_doc.get("synopsis"):
    self.description = cli_doc["synopsis"]
else:
    self.description = data.get("description")

# Add examples from metadata (these aren't in cli-doc)
if metadata and metadata.get("examples"):
    self.examples = metadata["examples"]
else:
    self.examples = data.get("examples")

# Add errors from metadata
if metadata and metadata.get("errors"):
    self.errors = metadata["errors"]
else:
    self.errors = []

# Add cross-references from metadata
if metadata:
    self.related_commands = metadata.get("related_commands", [])
    self.related_resources = metadata.get("related_resources", [])
else:
    self.related_commands = data.get("related_commands", [])
    self.related_resources = data.get("related_resources", [])
```

**Add helper**:
```python
def _get_metadata(self):
    """Get metadata for this command."""
    # Metadata stored by command path: "site create"
    parts = [self.name]
    if self.parent:
        parts.insert(0, self.parent.name)
    command_path = " ".join(parts)
    
    # Load from config/commands/metadata/
    metadata_dir = join(self.model.config_dir, "metadata")
    metadata_file = join(metadata_dir, f"{command_path.replace(' ', '-')}.yaml")
    
    if exists(metadata_file):
        return read_yaml(metadata_file)
    return {}
```

---

### Phase 5: Test All Commands (1 hour)

```bash
# Generate all commands
./plano generate

# Quick check: do they all generate?
ls input/commands/*/*.md | wc -l

# Spot check a few
cat input/commands/connector/create.md
cat input/commands/listener/status.md
cat input/commands/token/issue.md
```

---

## What We're NOT Doing (Keep It Simple)

❌ **Skip validation** - No enum checking, no warnings. Just make it work.  
❌ **Skip backward compatibility** - Don't keep old YAML fallbacks.  
❌ **Skip option merging complexity** - Just use cli-doc options directly.  
❌ **Skip property grouping** - metadata can have `group` field but don't implement it yet.  
❌ **Skip Resources/CRDs** - Do commands first, prove it works.  
❌ **Skip migration script** - Do it manually for one command first.

---

## Even Simpler: Hybrid Approach

**If the above is still too complex**, do this:

### Super Simple Mode: Keep YAML, Add cli-doc Validation

Don't change generation at all. Just add a check:

```python
# At the end of generation
def check_commands():
    """Warn if YAML has options not in cli-doc."""
    for command in model.commands:
        cli_doc = command._get_cli_doc_data()
        if cli_doc:
            yaml_options = {opt["name"] for opt in command.options}
            cli_options = {opt["name"] for opt in cli_doc["options"]}
            
            phantom = yaml_options - cli_options
            if phantom:
                warning(f"{command.name}: Options in YAML but not CLI: {phantom}")
```

This gives you the **validation benefits** without changing generation at all.

---

## Decision Point

**Which approach do you want?**

### Option A: Full Implementation (Phases 1-5)
- **Time**: ~3 hours
- **Benefit**: Actually uses cli-doc as source of truth
- **Risk**: Medium - changing core generation logic

### Option B: Super Simple Validation Only
- **Time**: ~30 minutes  
- **Benefit**: Find documentation errors
- **Risk**: Low - no generation changes
- **Limitation**: Doesn't fix the errors, just finds them

### Option C: One Command Proof of Concept
- **Time**: ~1 hour
- **Benefit**: Prove the approach works
- **Risk**: Low - only affects one command
- **Next Step**: Expand to all commands if successful

---

## Recommendation

**Start with Option C**: 
1. Modify `site create` command only
2. Hard-code it to use cli-doc
3. See if the output looks good
4. If yes, generalize to all commands
5. If no, iterate on the one command

**Code for Option C** (just for `site create`):

```python
class Command:
    def __init__(self, model, data):
        # HACK: Special case for site create
        if self.name == "create" and self.parent and self.parent.name == "site":
            cli_doc = model.cli_docs.get("site create")
            if cli_doc:
                self.description = cli_doc["synopsis"]
                self.options = cli_doc["options"]
                # Load metadata too
                metadata = read_yaml("config/commands/metadata/site-create.yaml")
                self.examples = metadata.get("examples", [])
        else:
            # Normal YAML-based logic for all other commands
            self.description = data.get("description")
            self.options = merge_yaml_options()
```

Test just that one command. If it works, remove the `if` and make it apply to all commands.

---

## Bottom Line

The simplest path:
1. ✅ **Load cli-doc** (30 min)
2. ✅ **Use it for one command** (1 hour)
3. ✅ **Test the output** (15 min)
4. ✅ **If good, expand to all** (1 hour)

**Total: ~3 hours to working system**

No validation, no fancy merging, no metadata initially. Just: does cli-doc → markdown generation work?
