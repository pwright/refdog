# CLI Commands Documentation: Proposal for cli-doc + Metadata Approach

## Executive Summary

**Situation**: Similar to the CRs/resources issue, CLI command documentation has two sources:
1. **cli-doc/*.md** - Auto-generated from Cobra CLI (source of truth for usage, flags, descriptions)
2. **config/commands/*.yaml** - Human-maintained metadata (examples, related commands, error messages, grouping)

**Recommendation**: Use a hybrid approach - parse cli-doc markdown files for authoritative CLI information, supplement with minimal metadata from config/commands.

**Benefits**:
- Single source of truth for CLI syntax and flags (cli-doc)
- No manual sync of flag descriptions
- Preserve documentation enhancements (examples, cross-references, error messages)
- Automatic updates when CLI changes

## Current Architecture

### What We Have Now

```
cli-doc/*.md (Auto-generated from Cobra)
    ↓
    (Currently not used directly)

config/commands/*.yaml (Human-maintained)
    ↓
python/commands.py (Generation)
    ↓
input/commands/*.md (Generated docs)
```

### Source Files

#### 1. cli-doc/*.md (Auto-generated from Cobra CLI)

**Location**: `cli-doc/`
**Source**: Skupper CLI (`cobra` command generates these)
**Format**: Markdown files, one per command/subcommand
**Content**:
- Command synopsis
- Usage syntax
- Flag descriptions
- Inherited flags
- Examples (basic)
- SEE ALSO links

**Examples**:
- `skupper_site_create.md`
- `skupper_listener_create.md`
- `skupper_connector_update.md`

**Key Characteristics**:
- ✅ Authoritative for CLI syntax
- ✅ Authoritative for flag descriptions
- ✅ Auto-updates when CLI changes
- ❌ Basic examples only
- ❌ No cross-references to resources/concepts
- ❌ No error message documentation
- ❌ No grouping/organization metadata

#### 2. config/commands/*.yaml (Human-maintained)

**Location**: `config/commands/`
**Format**: YAML files, one per command group
**Content**:
- Command descriptions (enhanced)
- Subcommand definitions
- Rich examples with explanations
- Related commands/resources
- Error messages and descriptions
- Option grouping (frequently-used, advanced)
- Wait conditions

**Examples**:
- `site.yaml`
- `listener.yaml`
- `connector.yaml`

**Key Characteristics**:
- ✅ Rich examples with context
- ✅ Cross-references to resources/concepts
- ✅ Error message documentation
- ✅ Option grouping
- ❌ Duplicates CLI flag descriptions
- ❌ Can get out of sync with actual CLI

## Comparison: cli-doc vs config/commands

### cli-doc/skupper_site_create.md provides:
```markdown
## skupper site create

Create a new site

### Synopsis
A site is a place where components of your application are running.
Sites are linked to form application networks.

### Options
      --enable-ha                 Configure the site for high availability
      --enable-link-access        allow access for incoming links
      --link-access-type string   configure external access for links
      --timeout duration          raise an error if operation times out
      --wait string               Wait for status (default "ready")
```

### config/commands/site.yaml provides:
```yaml
subcommands:
  - name: create
    wait: Ready
    description: Create a site.
    examples: |
      # Create a site
      $ skupper site create west
      Waiting for status...
      Site "west" is ready.

      # Create a site that can accept links
      $ skupper site create west --enable-link-access
    include_options: [site/*, create/*, context/*, global/*]
    errors:
      - message: A site resource already exists
        description: There is already a site resource defined
```

### What's Missing from cli-doc:

1. **Rich Examples**: cli-doc has basic examples, config has detailed ones with output
2. **Cross-References**: No links to related commands, resources, or concepts
3. **Error Documentation**: No error messages or troubleshooting
4. **Option Grouping**: No frequently-used vs advanced distinction
5. **Wait Conditions**: No documentation of what status to wait for
6. **Related Commands**: No links to related commands

### What's Duplicated:

1. **Flag Descriptions**: Both have them (cli-doc is authoritative)
2. **Command Descriptions**: Both have them (cli-doc is authoritative)
3. **Usage Syntax**: Both define it (cli-doc is authoritative)

## Proposed Architecture

### Hybrid Approach: cli-doc + Metadata

```
cli-doc/*.md (Source of truth for CLI)
    +
config/commands/metadata/*.yaml (Documentation metadata)
    ↓
python/commands.py (Enhanced parser + merger)
    ↓
input/commands/*.md (Generated docs)
```

### Metadata File Structure

Minimal metadata files that supplement cli-doc:

```yaml
# config/commands/metadata/site-create.yaml
command: site create

# Enhanced examples with context
examples:
  - description: Create a site
    command: skupper site create west
    output: |
      Waiting for status...
      Site "west" is ready.
  
  - description: Create a site that can accept links from remote sites
    command: skupper site create west --enable-link-access

# Cross-references
related_commands: [site/update, link/create]
related_resources: [site]
related_concepts: [site, network]
links: [skupper/site-configuration]

# Error documentation
errors:
  - message: A site resource already exists
    description: |
      There is already a site resource defined for the namespace.
      Use 'skupper site update' to modify the existing site.

# Option metadata (grouping, additional notes)
options:
  enable-link-access:
    group: frequently-used
    notes: Required if you want remote sites to link to this site
  
  enable-ha:
    group: advanced
    related_concepts: [high-availability]

# Wait condition documentation
wait:
  default: Ready
  description: |
    The create command waits for the site to reach Ready status by default.
```

## Implementation Plan

### Phase 1: Create CLI Parser

Create a parser to extract information from cli-doc markdown files:

```python
# python/cli_parser.py

def parse_cli_doc(markdown_file):
    """Parse a cli-doc markdown file"""
    with open(markdown_file) as f:
        content = f.read()
    
    # Extract sections
    command_info = {
        "name": extract_command_name(content),
        "synopsis": extract_synopsis(content),
        "usage": extract_usage(content),
        "options": extract_options(content),
        "inherited_options": extract_inherited_options(content),
        "examples": extract_examples(content),
        "see_also": extract_see_also(content),
    }
    
    return command_info

def extract_options(content):
    """Extract option flags and descriptions"""
    options = []
    in_options = False
    
    for line in content.split('\n'):
        if line.startswith('### Options'):
            in_options = True
            continue
        if in_options and line.startswith('###'):
            break
        if in_options and line.strip().startswith('--'):
            # Parse flag line
            option = parse_option_line(line)
            options.append(option)
    
    return options
```

### Phase 2: Create Metadata Files

Extract metadata from current config/commands/*.yaml:

```python
# scripts/extract_command_metadata.py

def extract_command_metadata(yaml_config):
    """Extract non-CLI data from command YAML"""
    metadata = {}
    
    for subcommand in yaml_config.get('subcommands', []):
        cmd_name = f"{yaml_config['name']}-{subcommand['name']}"
        
        cmd_metadata = {
            "command": f"{yaml_config['name']} {subcommand['name']}",
        }
        
        # Enhanced examples (not basic ones from cli-doc)
        if 'examples' in subcommand:
            cmd_metadata["examples"] = parse_examples(subcommand['examples'])
        
        # Cross-references
        if 'related_commands' in subcommand:
            cmd_metadata["related_commands"] = subcommand['related_commands']
        
        # Error documentation
        if 'errors' in subcommand:
            cmd_metadata["errors"] = subcommand['errors']
        
        # Option metadata (grouping, notes)
        if 'options' in subcommand:
            cmd_metadata["options"] = extract_option_metadata(subcommand['options'])
        
        # Wait conditions
        if 'wait' in subcommand:
            cmd_metadata["wait"] = {
                "default": subcommand['wait'],
                "description": f"Waits for {subcommand['wait']} status"
            }
        
        metadata[cmd_name] = cmd_metadata
    
    return metadata
```

### Phase 3: Merge CLI + Metadata

```python
# python/commands.py (enhanced)

class CommandModel:
    def __init__(self):
        # Load cli-doc markdown files
        self.cli_docs = {}
        for md_file in list_dir("cli-doc"):
            if md_file.endswith(".md"):
                cli_info = parse_cli_doc(join("cli-doc", md_file))
                self.cli_docs[cli_info["name"]] = cli_info
        
        # Load metadata files
        self.metadata = {}
        for yaml_file in list_dir("config/commands/metadata"):
            if yaml_file.endswith(".yaml"):
                meta = read_yaml(join("config/commands/metadata", yaml_file))
                self.metadata[meta["command"]] = meta
        
        # Merge
        self.commands = []
        for cmd_name, cli_info in self.cli_docs.items():
            metadata = self.metadata.get(cmd_name, {})
            command = Command(cli_info, metadata)
            self.commands.append(command)

class Command:
    def __init__(self, cli_info, metadata):
        # From cli-doc (authoritative)
        self.name = cli_info["name"]
        self.synopsis = cli_info["synopsis"]
        self.usage = cli_info["usage"]
        self.options = cli_info["options"]
        
        # From metadata (enhancements)
        self.enhanced_examples = metadata.get("examples", [])
        self.related_commands = metadata.get("related_commands", [])
        self.related_resources = metadata.get("related_resources", [])
        self.errors = metadata.get("errors", [])
        
        # Merge option metadata
        self.merge_option_metadata(metadata.get("options", {}))
    
    def merge_option_metadata(self, option_metadata):
        """Add grouping and notes to options from cli-doc"""
        for option in self.options:
            flag_name = option["name"]
            if flag_name in option_metadata:
                option["group"] = option_metadata[flag_name].get("group")
                option["notes"] = option_metadata[flag_name].get("notes")
                option["related_concepts"] = option_metadata[flag_name].get("related_concepts", [])
```

### Phase 4: Generate Documentation

```python
def generate_command(command):
    """Generate markdown for a command"""
    append = StringBuilder()
    
    # Title and usage (from cli-doc)
    append(f"# {command.title}")
    append()
    append("~~~ shell")
    append(command.usage)
    append("~~~")
    append()
    
    # Synopsis (from cli-doc)
    append(command.synopsis)
    append()
    
    # Enhanced examples (from metadata)
    if command.enhanced_examples:
        append("## Examples")
        append()
        for example in command.enhanced_examples:
            append(f"### {example['description']}")
            append()
            append("~~~ shell")
            append(example['command'])
            append("~~~")
            if 'output' in example:
                append()
                append("Output:")
                append()
                append("~~~ console")
                append(example['output'])
                append("~~~")
            append()
    
    # Options (from cli-doc + metadata grouping)
    append("## Options")
    append()
    
    # Group options
    for group in ["required", "frequently-used", None, "advanced"]:
        group_options = [opt for opt in command.options if opt.get("group") == group]
        if group_options:
            if group:
                append(f"### {group.replace('-', ' ').title()} options")
                append()
            for option in group_options:
                append(f"**`--{option['name']}`**")
                append()
                append(option['description'])
                if option.get('notes'):
                    append()
                    append(f"*Note: {option['notes']}*")
                append()
    
    # Error messages (from metadata)
    if command.errors:
        append("## Common Errors")
        append()
        for error in command.errors:
            append(f"### {error['message']}")
            append()
            append(error['description'])
            append()
    
    # Cross-references (from metadata)
    if command.related_commands or command.related_resources:
        append("## See Also")
        append()
        if command.related_commands:
            append("**Related commands:**")
            for cmd in command.related_commands:
                append(f"- [{cmd}]({cmd}.html)")
            append()
        if command.related_resources:
            append("**Related resources:**")
            for res in command.related_resources:
                append(f"- [{res}](../resources/{res}.html)")
            append()
    
    append.write(command.output_file)
```

## Validation

### Checks to Implement

1. **Missing Metadata**: Warn if cli-doc command has no metadata file
2. **Extra Metadata**: Warn if metadata file references non-existent command
3. **Option Mismatch**: Warn if metadata references options not in cli-doc
4. **Outdated Examples**: Warn if example commands don't match current usage syntax

```python
def validate_commands(model):
    """Validate cli-doc and metadata consistency"""
    
    # Check for missing metadata
    for cmd_name in model.cli_docs.keys():
        if cmd_name not in model.metadata:
            warning(f"Command '{cmd_name}' has no metadata file")
    
    # Check for extra metadata
    for cmd_name in model.metadata.keys():
        if cmd_name not in model.cli_docs:
            warning(f"Metadata for '{cmd_name}' has no corresponding cli-doc file")
    
    # Check option references
    for cmd_name, metadata in model.metadata.items():
        if cmd_name in model.cli_docs:
            cli_options = {opt["name"] for opt in model.cli_docs[cmd_name]["options"]}
            meta_options = set(metadata.get("options", {}).keys())
            
            extra = meta_options - cli_options
            if extra:
                warning(f"{cmd_name}: Metadata references non-existent options: {extra}")
```

## Migration Steps

### Step 1: Extract Metadata

```bash
# Run extraction script
python scripts/extract_command_metadata.py

# Creates config/commands/metadata/*.yaml files
```

### Step 2: Implement Parser

```bash
# Implement cli-doc parser
# Add to python/cli_parser.py
```

### Step 3: Update CommandModel

```bash
# Modify python/commands.py to use cli-doc + metadata
```

### Step 4: Test

```bash
# Generate with new system
./plano generate

# Compare output with current system
diff -r input/commands/ input/commands.backup/
```

### Step 5: Migrate

```bash
# Once satisfied, remove old config/commands/*.yaml
# Keep only config/commands/metadata/*.yaml
```

## Benefits

1. **Single Source of Truth**: cli-doc is authoritative for CLI syntax
2. **Automatic Updates**: When CLI changes, cli-doc updates automatically
3. **No Manual Sync**: Flag descriptions come from CLI, not duplicated
4. **Preserved Enhancements**: Examples, cross-references, errors remain
5. **Smaller Metadata**: ~70% reduction in metadata file size
6. **Better Consistency**: CLI docs always match actual CLI

## Comparison: Current vs New

### Current (config/commands/site.yaml)
```yaml
# ~122 lines
name: site
resource: site
description: Display help for site commands
subcommands:
  - name: create
    description: Create a site.
    examples: |
      # Create a site
      $ skupper site create west
    options:
      - name: name
        description: A name of your choice for the Skupper site
      - name: enable-link-access
        type: boolean
        description: Allow access for incoming links
    # ... many more lines
```

### New (config/commands/metadata/site-create.yaml)
```yaml
# ~35 lines (71% reduction)
command: site create

examples:
  - description: Create a site
    command: skupper site create west
    output: |
      Waiting for status...
      Site "west" is ready.

related_commands: [site/update, link/create]
related_resources: [site]

errors:
  - message: A site resource already exists
    description: There is already a site resource defined

options:
  enable-link-access:
    group: frequently-used
```

## Estimated Effort

- **Phase 1** (CLI Parser): 4-6 hours
- **Phase 2** (Extract Metadata): 2-3 hours
- **Phase 3** (Merge Logic): 6-8 hours
- **Phase 4** (Generation): 4-6 hours
- **Testing & Migration**: 4-6 hours

**Total**: 20-29 hours

## Recommendation

**Proceed with cli-doc + metadata approach** for the same reasons as the CRD approach:
- Authoritative source (cli-doc from actual CLI)
- Minimal metadata for documentation enhancements
- Automatic consistency
- Reduced maintenance burden

This gives you a unified approach for both resources (CRD + metadata) and commands (cli-doc + metadata).