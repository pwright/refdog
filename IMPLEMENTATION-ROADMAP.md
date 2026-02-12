# Implementation Roadmap: Documentation Generation System

## Executive Summary

This document provides a complete roadmap for implementing the new documentation generation system for both Resources (CRs) and CLI Commands.

**Current Status**: Foundation complete (Phases 1-2 for both systems)
**Remaining Work**: Merge logic implementation and testing (Phases 3-5)
**Estimated Effort**: 26-36 hours total remaining

## What Has Been Completed

### Resources (CRs) System

#### ✅ Phase 1-2: Foundation (COMPLETE)
- **Documentation created**:
  - `resources.md` - Current processes
  - `crd-generation-proposal.md` - Strategic proposal
  - `example-metadata-site.yaml` - Reference example
  - `generation-merge-logic.md` - Technical implementation guide

- **Infrastructure ready**:
  - `config/resources/metadata/` - Directory created
  - 9 metadata files extracted from current YAML configs
  - `scripts/extract_metadata_standalone.py` - Migration tool
  - `python/common.py` - Fixed to skip metadata directory

#### ⏳ Phase 3-5: Implementation (PENDING)
**Estimated**: 16-24 hours

**Tasks**:
1. Implement new ResourceModel to load CRDs + metadata
2. Add Property class with merge logic
3. Update generation functions
4. Add validation (enum mismatches, etc.)
5. Test with Site resource
6. Migrate remaining resources
7. Update documentation

### CLI Commands System

#### ✅ Phase 1: CLI Parser (COMPLETE)
- **Deliverable**: `python/cli_parser.py`
- **Test tool**: `scripts/test_cli_parser.py`
- **Results**: 38/39 commands parsed successfully
- **Capabilities**:
  - Parses cli-doc markdown (Cobra-generated)
  - Extracts all command information
  - Handles multiple option formats
  - Infers types and extracts defaults/choices

#### ✅ Phase 2: Metadata Extraction (COMPLETE)
- **Deliverable**: `scripts/extract_command_metadata_standalone.py`
- **Results**: 31 command metadata files created
- **Location**: `config/commands/metadata/`
- **Content**: Examples, cross-references, errors, wait conditions

#### ⏳ Phase 3-4: Implementation (PENDING)
**Estimated**: 10-12 hours

**Tasks**:
1. Implement CommandModel to load cli-doc + metadata
2. Add merge logic for commands
3. Update generation functions
4. Add validation
5. Test with site create command
6. Migrate remaining commands

## Implementation Priority

### Option A: Implement Resources First (Recommended)
**Rationale**: 
- More critical (API documentation)
- Clearer requirements
- Existing validation framework

**Timeline**:
1. Week 1-2: Resources implementation (16-24 hours)
2. Week 3: CLI Commands implementation (10-12 hours)
3. Week 4: Testing and documentation

### Option B: Implement CLI Commands First
**Rationale**:
- Simpler (no CRD schema complexity)
- Good proof of concept
- Faster initial results

**Timeline**:
1. Week 1: CLI Commands implementation (10-12 hours)
2. Week 2-3: Resources implementation (16-24 hours)
3. Week 4: Testing and documentation

### Option C: Parallel Implementation
**Rationale**:
- Fastest overall completion
- Requires 2 developers

**Timeline**:
1. Week 1-2: Both systems in parallel
2. Week 3: Integration and testing

## Detailed Implementation Steps

### Resources System (Phase 3-5)

#### Step 1: Implement ResourceModel Changes (6-8 hours)

**File**: `python/resources.py`

**Changes needed**:
```python
class ResourceModel(Model):
    def __init__(self):
        # Load CRDs (already exists)
        self.crds_by_name = {}
        for crd_file in list_dir("crds"):
            # ... existing code ...
        
        # NEW: Load metadata files
        self.metadata_by_name = {}
        for metadata_file in list_dir("config/resources/metadata"):
            if metadata_file.endswith(".yaml"):
                metadata = read_yaml(join("config/resources/metadata", metadata_file))
                self.metadata_by_name[metadata["name"]] = metadata
        
        # NEW: Create resources by merging CRD + metadata
        self.resources = []
        for kind, crd_data in self.crds_by_name.items():
            metadata = self.metadata_by_name.get(kind, {})
            resource = Resource(self, crd_data, metadata)
            self.resources.append(resource)

class Resource(ModelObject):
    def __init__(self, model, crd_data, metadata):
        # From CRD (authoritative)
        schema = crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
        self.name = crd_data["spec"]["names"]["kind"]
        self.description = schema.get("description", "")
        
        # From metadata (enhancements)
        self.examples = metadata.get("examples", [])
        self.related_resources = metadata.get("related_resources", [])
        self.related_concepts = metadata.get("related_concepts", [])
        self.links = metadata.get("links", [])
        
        # Build properties by merging
        self.spec_properties = []
        spec_schema = schema["properties"]["spec"]["properties"]
        metadata_props = metadata.get("properties", {})
        
        for prop_name, prop_schema in spec_schema.items():
            prop = self._create_property(
                name=prop_name,
                schema=prop_schema,
                metadata=metadata_props.get(prop_name, {}),
                section="spec"
            )
            self.spec_properties.append(prop)
        
        # Same for status properties
        # ...
```

#### Step 2: Add Validation (2-3 hours)

**Add to ResourceModel.check()**:
```python
def check(self):
    # Existing checks...
    
    # NEW: Check for enum mismatches
    for resource in self.resources:
        for prop in resource.spec_properties + resource.status_properties:
            if prop.enum:
                crd_values = set(prop.enum)
                metadata_values = set(c["name"] for c in prop.choices)
                
                extra = metadata_values - crd_values
                if extra:
                    warning(f"{resource.name}.{prop.name}: Metadata defines choices not in CRD: {extra}")
                
                missing = crd_values - metadata_values
                if missing:
                    warning(f"{resource.name}.{prop.name}: CRD enum values lack metadata: {missing}")
```

#### Step 3: Test with Site Resource (2-3 hours)

```bash
# Backup current output
cp -r input/resources input/resources.backup

# Generate with new system
./plano generate

# Compare
diff input/resources/site.md input/resources.backup/site.md

# Review warnings
./plano generate 2>&1 | grep -i warning
```

#### Step 4: Migrate Remaining Resources (4-6 hours)

- Review each resource's metadata file
- Remove redundant descriptions (now in CRDs)
- Test generation for each
- Fix any issues

#### Step 5: Update Documentation (2-3 hours)

- Update resources.md with new process
- Add troubleshooting section
- Document validation warnings

### CLI Commands System (Phase 3-4)

#### Step 1: Implement CommandModel (4-6 hours)

**File**: `python/commands.py`

**Changes needed**:
```python
from cli_parser import parse_all_cli_docs

class CommandModel(Model):
    def __init__(self):
        # NEW: Load cli-doc files
        self.cli_docs = parse_all_cli_docs("cli-doc")
        
        # NEW: Load metadata files
        self.metadata = {}
        for yaml_file in list_dir("config/commands/metadata"):
            if yaml_file.endswith(".yaml"):
                meta = read_yaml(join("config/commands/metadata", yaml_file))
                self.metadata[meta["command"]] = meta
        
        # NEW: Merge to create commands
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
```

#### Step 2: Update Generation (2-3 hours)

**Update generate_command() function**:
```python
def generate_command(command):
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
    # ... group by frequently-used, advanced, etc.
    
    # Error messages (from metadata)
    # Cross-references (from metadata)
    # ...
```

#### Step 3: Test with site create (1-2 hours)

```bash
# Backup
cp -r input/commands input/commands.backup

# Generate
./plano generate

# Compare
diff input/commands/site/create.md input/commands.backup/site/create.md
```

#### Step 4: Migrate Remaining Commands (2-3 hours)

- Test all commands
- Fix any parsing issues
- Verify cross-references

## Testing Strategy

### Unit Tests
- Test CRD parser
- Test cli-doc parser
- Test merge logic
- Test validation

### Integration Tests
- Generate all resources
- Generate all commands
- Compare with current output
- Verify no regressions

### Manual Review
- Check one resource from each type
- Check one command from each group
- Verify examples render correctly
- Test cross-references

## Rollback Plan

If issues arise:

1. **Keep old system working**: Don't delete old YAML configs until new system is proven
2. **Feature flag**: Add environment variable to switch between old/new
3. **Gradual migration**: Migrate one resource/command at a time
4. **Backup outputs**: Keep generated files from old system for comparison

## Success Criteria

### Resources System
- [ ] All 9 resources generate correctly
- [ ] No validation warnings (or all explained)
- [ ] Output matches or improves current docs
- [ ] Cross-references work
- [ ] Examples render correctly

### CLI Commands System
- [ ] All 31 commands generate correctly
- [ ] No parsing errors
- [ ] Enhanced examples display properly
- [ ] Option grouping works
- [ ] Error documentation included

## Risk Mitigation

### Risk 1: CRD Descriptions Insufficient
**Mitigation**: Keep ability to override in metadata

### Risk 2: Breaking Changes
**Mitigation**: Extensive testing, gradual rollout

### Risk 3: Performance Issues
**Mitigation**: Profile generation time, optimize if needed

### Risk 4: Maintenance Burden
**Mitigation**: Good documentation, clear processes

## Next Steps

### Immediate (This Week)
1. Choose implementation priority (A, B, or C)
2. Set up development branch
3. Begin Phase 3 implementation

### Short Term (Next 2-4 Weeks)
1. Complete implementation
2. Testing and validation
3. Documentation updates

### Long Term (Next Month)
1. Monitor for issues
2. Gather feedback
3. Iterate and improve

## Resources Needed

- **Developer Time**: 26-36 hours
- **Review Time**: 4-6 hours
- **Testing Environment**: Existing setup sufficient
- **Documentation**: This roadmap + existing proposals

## Questions to Answer

1. Which implementation priority (A, B, or C)?
2. Who will implement (1 or 2 developers)?
3. What's the timeline/deadline?
4. Any specific concerns or requirements?

## Conclusion

The foundation is complete. All design work, documentation, and preparation is done. The remaining work is straightforward implementation following the detailed specifications provided.

**Recommendation**: Start with CLI Commands (Option B) as a proof of concept, then proceed to Resources. This provides faster initial results and validates the approach before tackling the more complex Resources system.

**Estimated Total Time to Completion**: 4-6 weeks with 1 developer working part-time, or 2-3 weeks full-time.