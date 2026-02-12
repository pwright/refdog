# Command Merge Logic Implementation Guide

## Overview

This document provides a complete implementation guide for merging cli-doc (authoritative) with metadata (enhancements) for CLI command documentation.

## Current State

### What Exists
- ✅ cli-doc files (38 markdown files from Cobra)
- ✅ CLI parser (`python/cli_parser.py`) - extracts data from cli-doc
- ✅ Metadata files (30 YAML files in `config/commands/metadata/`)
- ✅ Validation script - confirms 100% alignment
- ✅ Current generation system (`python/commands.py`)

### What Needs Implementation
- ⏳ Modified `CommandModel` to load cli-doc + metadata
- ⏳ Merge logic in `Command` class
- ⏳ Updated generation to use merged data
- ⏳ Testing and migration

## Implementation Strategy

### Phase 1: Add cli-doc Loading (2-3 hours)

#### Step 1.1: Import CLI Parser

**File**: `python/commands.py`

Add at top of file:
```python
from cli_parser import parse_cli_doc_file, parse_all_cli_docs
```

#### Step 1.2: Modify CommandModel.__init__

**Current code** (lines 224-229):
```python
class CommandModel(Model):
    def __init__(self):
        super().__init__(Command, "config/commands")
        
        self.option_data = read_yaml(join(self.config_dir, "options.yaml"))
        
        self.init(exclude=["options.yaml", "overview.md"])
```

**New code**:
```python
class CommandModel(Model):
    def __init__(self):
        super().__init__(Command, "config/commands")
        
        self.option_data = read_yaml(join(self.config_dir, "options.yaml"))
        
        # NEW: Load cli-doc files
        self.cli_doc_dir = "cli-doc"
        self.cli_docs = {}
        
        if exists(self.cli_doc_dir):
            notice("Loading cli-doc files...")
            try:
                self.cli_docs = parse_all_cli_docs(self.cli_doc_dir)
                notice(f"Loaded {len(self.cli_docs)} cli-doc files")
            except Exception as e:
                warning(f"Failed to load cli-doc files: {e}")
                warning("Falling back to YAML-only mode")
        
        # NEW: Load metadata files
        self.metadata_dir = join(self.config_dir, "metadata")
        self.metadata = {}
        
        if exists(self.metadata_dir):
            notice("Loading command metadata...")
            for yaml_file in list_dir(self.metadata_dir):
                if yaml_file.endswith(".yaml"):
                    path = join(self.metadata_dir, yaml_file)
                    data = read_yaml(path)
                    if data and "command" in data:
                        self.metadata[data["command"]] = data
            notice(f"Loaded {len(self.metadata)} metadata files")
        
        self.init(exclude=["options.yaml", "overview.md", "metadata"])
```

#### Step 1.3: Add Helper Method

Add to `CommandModel` class:
```python
def get_cli_doc(self, command_name):
    """Get cli-doc data for a command."""
    # Try full command name first
    if command_name in self.cli_docs:
        return self.cli_docs[command_name]
    
    # Try with 'skupper ' prefix
    full_name = f"skupper {command_name}"
    if full_name in self.cli_docs:
        return self.cli_docs[full_name]
    
    return None

def get_metadata(self, command_name):
    """Get metadata for a command."""
    return self.metadata.get(command_name, {})
```

### Phase 2: Implement Merge Logic (3-4 hours)

#### Step 2.1: Modify Command.__init__

**Current approach**: Loads from YAML data only

**New approach**: Merge cli-doc + metadata + YAML

Add to `Command.__init__` (after line 258):
```python
def __init__(self, model, data, parent=None):
    super().__init__(model, data)
    
    self.parent = parent
    self.subcommands = list()
    
    # NEW: Get cli-doc and metadata
    command_path = self._get_command_path()
    self.cli_doc_data = model.get_cli_doc(command_path)
    self.metadata_data = model.get_metadata(command_path)
    
    # NEW: Merge data sources
    self._merge_command_data()
    
    # Rest of existing code...
    self.options = list()
    # ...
```

#### Step 2.2: Add Merge Methods

Add these methods to `Command` class:

```python
def _get_command_path(self):
    """Get the full command path (e.g., 'site create')."""
    parts = []
    for ancestor in reversed(list(self.ancestors)):
        parts.append(ancestor.name)
    parts.append(self.name)
    return " ".join(parts)

def _merge_command_data(self):
    """Merge cli-doc, metadata, and YAML data."""
    # Priority: YAML > metadata > cli-doc
    
    # Start with cli-doc (if available)
    if self.cli_doc_data:
        # Use cli-doc synopsis if no description in YAML
        if not self.data.get("description") and self.cli_doc_data.get("synopsis"):
            self.data.setdefault("description", self.cli_doc_data["synopsis"])
        
        # Use cli-doc usage if not in YAML
        if not self.data.get("usage") and self.cli_doc_data.get("usage"):
            self.data.setdefault("usage", self.cli_doc_data["usage"])
    
    # Layer on metadata enhancements
    if self.metadata_data:
        # Enhanced examples from metadata
        if "examples" in self.metadata_data and not self.data.get("examples"):
            self.data["enhanced_examples"] = self.metadata_data["examples"]
        
        # Wait conditions from metadata
        if "wait" in self.metadata_data and not self.data.get("wait"):
            wait_data = self.metadata_data["wait"]
            if isinstance(wait_data, dict):
                self.data["wait"] = wait_data.get("default")
                self.data["wait_description"] = wait_data.get("description")
            else:
                self.data["wait"] = wait_data
        
        # Errors from metadata
        if "errors" in self.metadata_data:
            self.data.setdefault("errors", self.metadata_data["errors"])
        
        # Related items from metadata
        for key in ["related_commands", "related_resources", "related_concepts"]:
            if key in self.metadata_data:
                self.data.setdefault(key, self.metadata_data[key])
```

#### Step 2.3: Merge Options

Modify `merge_option_data()` method:

```python
def merge_option_data(self):
    """Merge options from cli-doc, metadata, and YAML."""
    # Start with existing YAML-based merge
    yaml_options = self._merge_yaml_options()
    
    # If no cli-doc, return YAML options
    if not self.cli_doc_data:
        return yaml_options
    
    # Get cli-doc options
    cli_doc_options = self.cli_doc_data.get("options", [])
    cli_doc_by_name = {opt["name"]: opt for opt in cli_doc_options}
    
    # Get metadata options
    metadata_options = self.metadata_data.get("options", {})
    
    # Build merged options
    merged = []
    yaml_by_name = {opt["name"]: opt for opt in yaml_options}
    
    # Process all options from cli-doc (authoritative for existence)
    for cli_opt in cli_doc_options:
        name = cli_opt["name"]
        
        # Start with cli-doc data
        merged_opt = dict(cli_opt)
        
        # Layer on metadata enhancements
        if name in metadata_options:
            meta_opt = metadata_options[name]
            # Add grouping from metadata
            if "group" in meta_opt:
                merged_opt["group"] = meta_opt["group"]
            # Add enhanced description from metadata
            if "description" in meta_opt:
                merged_opt["description"] = meta_opt["description"]
        
        # Layer on YAML overrides (highest priority)
        if name in yaml_by_name:
            yaml_opt = yaml_by_name[name]
            merged_opt.update(yaml_opt)
        
        merged.append(merged_opt)
    
    # Add any YAML-only options (for backward compatibility)
    for name, yaml_opt in yaml_by_name.items():
        if name not in cli_doc_by_name:
            merged.append(yaml_opt)
    
    return merged

def _merge_yaml_options(self):
    """Original YAML-based option merging (for backward compatibility)."""
    model_options = self.model.option_data
    included_keys = list()
    
    for pattern in self.data.get("include_options", []):
        for key in model_options:
            if string_matches_glob(key, pattern):
                included_keys.append(key)
    
    for pattern in self.data.get("exclude_options", []):
        for key in included_keys:
            if string_matches_glob(key, pattern):
                included_keys.remove(key)
    
    included_options = {model_options[x]["name"]: model_options[x] for x in included_keys}
    specific_options = {x["name"]: x for x in self.data.get("options", [])}
    
    included_names = [x for x in included_options if x not in specific_options]
    merged_names = list(specific_options.keys()) + included_names
    merged_options = list()
    
    for name in merged_names:
        included_data = included_options.get(name, {})
        specific_data = specific_options.get(name, {})
        
        merged_data = dict(included_data)
        merged_data.update(specific_data)
        
        if "description" in included_data and "description" in specific_data:
            included_description = included_data["description"]
            specific_description = specific_data["description"]
            merged_data["description"] = specific_description.replace("@description@", included_description)
        
        merged_options.append(merged_data)
    
    return merged_options
```

### Phase 3: Update Generation (2-3 hours)

#### Step 3.1: Enhanced Examples

Modify `generate_command()` function (around line 100):

**Current code**:
```python
if command.examples:
    append("## Examples")
    append()
    append("~~~ console")
    append(command.examples.strip())
    append("~~~")
    append()
```

**New code**:
```python
# Check for enhanced examples from metadata
enhanced_examples = command.data.get("enhanced_examples")

if enhanced_examples:
    append("## Examples")
    append()
    
    for example in enhanced_examples:
        if "description" in example:
            append(f"### {example['description']}")
            append()
        
        append("~~~ shell")
        append(example["command"])
        append("~~~")
        
        if "output" in example:
            append()
            append("Output:")
            append()
            append("~~~ console")
            append(example["output"])
            append("~~~")
        
        append()
elif command.examples:
    # Fallback to simple examples
    append("## Examples")
    append()
    append("~~~ console")
    append(command.examples.strip())
    append("~~~")
    append()
```

#### Step 3.2: Wait Conditions

Modify `generate_command_fields()` (around line 153):

**Current code**:
```python
def generate_command_fields(command):
    rows = list()
    
    rows.append(f"<tr><th>Platforms</th><td>{', '.join(command.platforms)}</td>")
    
    if command.wait:
        rows.append(f"<tr><th>Waits for</th><td>{command.wait}</td>")
    
    return f"<table class=\"fields\">{''.join(rows)}</table>"
```

**New code**:
```python
def generate_command_fields(command):
    rows = list()
    
    rows.append(f"<tr><th>Platforms</th><td>{', '.join(command.platforms)}</td>")
    
    if command.wait:
        wait_text = command.wait
        wait_desc = command.data.get("wait_description")
        if wait_desc:
            wait_text = f"{wait_text} - {wait_desc}"
        rows.append(f"<tr><th>Waits for</th><td>{wait_text}</td>")
    
    return f"<table class=\"fields\">{''.join(rows)}</table>"
```

### Phase 4: Add Validation (1-2 hours)

Add to `CommandModel.check()`:

```python
def check(self):
    # Existing checks...
    for command in self.commands:
        for option in command.options:
            if not option.name:
                fail(f"{command}: {option} has no name")
            
            if not option.type:
                fail(f"{command}: {option} has no type")
        
        # ... existing subcommand checks ...
    
    # NEW: Validate cli-doc alignment
    if self.cli_docs:
        self._validate_cli_doc_alignment()

def _validate_cli_doc_alignment(self):
    """Validate that metadata aligns with cli-doc."""
    warnings_found = 0
    
    for command_name, metadata in self.metadata.items():
        cli_doc = self.get_cli_doc(command_name)
        
        if not cli_doc:
            warning(f"Metadata exists for '{command_name}' but no cli-doc found")
            warnings_found += 1
            continue
        
        # Check options
        cli_doc_options = {opt["name"]: opt for opt in cli_doc.get("options", [])}
        metadata_options = metadata.get("options", {})
        
        for opt_name in metadata_options:
            if opt_name not in cli_doc_options:
                warning(f"{command_name}: Option '{opt_name}' in metadata but not in cli-doc")
                warnings_found += 1
    
    if warnings_found > 0:
        notice(f"Found {warnings_found} cli-doc alignment warnings")
```

### Phase 5: Testing (2-3 hours)

#### Test Plan

1. **Unit Test**: Test merge logic with sample data
2. **Integration Test**: Generate one command and compare
3. **Full Test**: Generate all commands
4. **Regression Test**: Compare with current output

#### Test Script

Create `scripts/test_command_merge.py`:

```python
#!/usr/bin/env python3
"""Test command merge logic."""

import sys
from pathlib import Path

# Add python directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from commands import CommandModel

def test_merge():
    print("Testing command merge logic...")
    
    # Load model
    model = CommandModel()
    
    # Test specific command
    site_create = None
    for cmd in model.commands:
        if cmd.name == "site":
            for subcmd in cmd.subcommands:
                if subcmd.name == "create":
                    site_create = subcmd
                    break
    
    if not site_create:
        print("ERROR: Could not find 'site create' command")
        return 1
    
    print(f"\nCommand: {site_create.title}")
    print(f"Description: {site_create.description[:100]}...")
    print(f"Options: {len(site_create.options)}")
    print(f"Examples: {len(site_create.data.get('enhanced_examples', []))}")
    print(f"Errors: {len(site_create.errors)}")
    
    # Check cli-doc data was loaded
    if site_create.cli_doc_data:
        print("\n✅ cli-doc data loaded")
    else:
        print("\n⚠️  No cli-doc data")
    
    # Check metadata was loaded
    if site_create.metadata_data:
        print("✅ Metadata loaded")
    else:
        print("⚠️  No metadata")
    
    print("\n✅ Merge logic test passed")
    return 0

if __name__ == "__main__":
    sys.exit(test_merge())
```

Run test:
```bash
python scripts/test_command_merge.py
```

#### Comparison Test

```bash
# Backup current output
cp -r input/commands input/commands.backup

# Generate with new system
./plano generate

# Compare
diff -r input/commands input/commands.backup

# Check specific file
diff input/commands/site/create.md input/commands.backup/site/create.md
```

### Phase 6: Migration (1-2 hours)

#### Migration Steps

1. **Backup**: Save current YAML configs
2. **Test**: Verify generation works
3. **Review**: Check output quality
4. **Iterate**: Fix any issues
5. **Document**: Update documentation

#### Rollback Plan

If issues arise:

```python
# Add feature flag to CommandModel
class CommandModel(Model):
    def __init__(self, use_cli_doc=True):
        self.use_cli_doc = use_cli_doc and exists("cli-doc")
        
        if not self.use_cli_doc:
            notice("Using YAML-only mode (cli-doc disabled)")
        
        # ... rest of init
```

Enable/disable:
```python
# In generate.py or wherever CommandModel is instantiated
model = CommandModel(use_cli_doc=False)  # Disable for rollback
```

## Benefits After Implementation

### Immediate Benefits
- Single source of truth (cli-doc from Cobra)
- Automatic sync with CLI changes
- Reduced maintenance burden
- Better consistency

### Long-term Benefits
- Easier to add new commands
- Less duplication
- Clearer separation of concerns
- Better validation

## Estimated Effort

| Phase | Task | Hours |
|-------|------|-------|
| 1 | Add cli-doc loading | 2-3 |
| 2 | Implement merge logic | 3-4 |
| 3 | Update generation | 2-3 |
| 4 | Add validation | 1-2 |
| 5 | Testing | 2-3 |
| 6 | Migration | 1-2 |
| **Total** | | **11-17 hours** |

## Success Criteria

- [ ] All 30 commands generate correctly
- [ ] Enhanced examples display properly
- [ ] Option grouping works
- [ ] Error documentation included
- [ ] Wait conditions shown
- [ ] Cross-references work
- [ ] No validation warnings
- [ ] Output matches or improves current docs

## Next Steps

1. Review this implementation guide
2. Set up development branch
3. Implement Phase 1 (cli-doc loading)
4. Test Phase 1
5. Proceed to Phase 2
6. Continue through all phases

## Notes

- Keep YAML configs during transition for rollback
- Test incrementally after each phase
- Document any deviations from this plan
- Update this guide as implementation progresses

---

**Status**: Ready for implementation  
**Prerequisites**: All complete (parser, metadata, validation)  
**Risk Level**: Low (can rollback to YAML-only mode)