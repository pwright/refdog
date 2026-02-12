# How CRD + Metadata Merging Works

This document explains how the generation system would merge CRD content with static metadata files to produce complete documentation.

## Data Flow

```
┌─────────────────────────┐
│  CRD File               │
│  (skupper_site_crd.yaml)│
│                         │
│  Provides:              │
│  • Descriptions         │
│  • Types                │
│  • Required fields      │
│  • Validation rules     │
│  • Default values       │
└───────────┬─────────────┘
            │
            │ MERGE
            ↓
┌─────────────────────────┐     ┌─────────────────────────┐
│  Metadata File          │────→│  Generated Markdown     │
│  (metadata/site.yaml)   │     │  (input/resources/      │
│                         │     │   site.md)              │
│  Provides:              │     │                         │
│  • Examples             │     │  Contains:              │
│  • Property grouping    │     │  • Full descriptions    │
│  • Cross-references     │     │  • Organized properties │
│  • External links       │     │  • Examples             │
│  • Updatable flags      │     │  • Cross-references     │
│  • Platform notes       │     │  • All metadata         │
│  • Choice descriptions  │     └─────────────────────────┘
└─────────────────────────┘
```

## Merge Logic by Field

### Resource-Level Fields

| Field | Source | Notes |
|-------|--------|-------|
| **name** | CRD `spec.names.kind` | Authoritative |
| **description** | CRD `openAPIV3Schema.description` | Main description from CRD |
| **examples** | Metadata `examples` | Static content only |
| **related_resources** | Metadata `related_resources` | Static content only |
| **related_concepts** | Metadata `related_concepts` | Static content only |
| **links** | Metadata `links` | Static content only |

### Property-Level Fields

| Field | Source | Merge Strategy |
|-------|--------|----------------|
| **name** | CRD schema | Authoritative |
| **type** | CRD `type` | Authoritative |
| **format** | CRD `format` | Authoritative |
| **description** | CRD `description` | **Primary source** |
| **required** | CRD `required` array | Authoritative |
| **default** | CRD `default` | Authoritative (if present) |
| **enum** | CRD `enum` | Authoritative |
| **group** | Metadata `properties[name].group` | Static only |
| **updatable** | Metadata `properties[name].updatable` | Static only |
| **platforms** | Metadata `properties[name].platforms` | Static only |
| **related_concepts** | Metadata `properties[name].related_concepts` | Static only |
| **related_resources** | Metadata `properties[name].related_resources` | Static only |
| **links** | Metadata `properties[name].links` | Static only |
| **choices** | **MERGE**: CRD enum + Metadata descriptions | See below |

### Choice/Enum Handling (Special Case)

For enum properties, we merge CRD enum values with metadata descriptions:

**CRD provides**:
```yaml
linkAccess:
  type: string
  enum: [none, default, route, loadbalancer]
```

**Metadata provides**:
```yaml
linkAccess:
  choices:
    - name: none
      description: No linking to this site is permitted.
    - name: default
      platforms: [Kubernetes]
      description: Use the default link access...
```

**Result**: Each enum value gets its detailed description and platform notes.

## Code Implementation Example

```python
class ResourceModel(Model):
    def __init__(self):
        # Load CRDs
        self.crds_by_name = {}
        for crd_file in list_dir("crds"):
            crd_data = read_yaml(join("crds", crd_file))
            if crd_data["kind"] == "CustomResourceDefinition":
                kind = crd_data["spec"]["names"]["kind"]
                self.crds_by_name[kind] = crd_data
        
        # Load metadata files
        self.metadata_by_name = {}
        for metadata_file in list_dir("config/resources/metadata"):
            metadata = read_yaml(join("config/resources/metadata", metadata_file))
            self.metadata_by_name[metadata["name"]] = metadata
        
        # Create Resource objects by merging
        self.resources = []
        for kind, crd_data in self.crds_by_name.items():
            metadata = self.metadata_by_name.get(kind, {})
            resource = Resource(self, crd_data, metadata)
            self.resources.append(resource)

class Resource(ModelObject):
    def __init__(self, model, crd_data, metadata):
        # Resource-level fields
        self.name = crd_data["spec"]["names"]["kind"]
        
        # Description from CRD
        schema = crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
        self.description = schema.get("description", "")
        
        # Documentation metadata from metadata file
        self.examples = metadata.get("examples", [])
        self.related_resources = metadata.get("related_resources", [])
        self.related_concepts = metadata.get("related_concepts", [])
        self.links = metadata.get("links", [])
        
        # Build properties by merging CRD schema with metadata
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
        self.status_properties = []
        status_schema = schema["properties"]["status"]["properties"]
        
        for prop_name, prop_schema in status_schema.items():
            prop = self._create_property(
                name=prop_name,
                schema=prop_schema,
                metadata=metadata_props.get(prop_name, {}),
                section="status"
            )
            self.status_properties.append(prop)
    
    def _create_property(self, name, schema, metadata, section):
        """Merge CRD schema with metadata for a single property"""
        return Property(
            name=name,
            # From CRD
            type=schema.get("type"),
            format=schema.get("format"),
            description=schema.get("description", ""),
            default=schema.get("default"),
            enum=schema.get("enum", []),
            # From metadata
            group=metadata.get("group"),
            updatable=metadata.get("updatable", False),
            platforms=metadata.get("platforms", []),
            related_concepts=metadata.get("related_concepts", []),
            related_resources=metadata.get("related_resources", []),
            links=metadata.get("links", []),
            choices=self._merge_choices(schema.get("enum", []), metadata.get("choices", [])),
            section=section
        )
    
    def _merge_choices(self, enum_values, choice_metadata):
        """Merge CRD enum values with metadata choice descriptions"""
        if not enum_values:
            return []
        
        # Create a map of choice metadata by name
        choice_map = {c["name"]: c for c in choice_metadata}
        
        # VALIDATION: Check for mismatches
        crd_values = set(enum_values)
        metadata_values = set(choice_map.keys())
        
        # Warn about extra choices in metadata (not in CRD)
        extra_in_metadata = metadata_values - crd_values
        if extra_in_metadata:
            warning(f"{self.name}.{name}: Metadata defines choices not in CRD enum: {extra_in_metadata}")
        
        # Warn about missing choices in metadata (in CRD but no description)
        missing_in_metadata = crd_values - metadata_values
        if missing_in_metadata:
            warning(f"{self.name}.{name}: CRD enum values lack metadata descriptions: {missing_in_metadata}")
        
        # Build merged choices (only include values that exist in CRD)
        choices = []
        for value in enum_values:
            choice = {"name": value}
            if value in choice_map:
                # Add metadata if available
                choice.update(choice_map[value])
            else:
                # No metadata for this enum value - will use CRD description if available
                debug(f"{self.name}.{name}: Using CRD description for choice '{value}'")
            choices.append(choice)
        
        return choices

class Property:
    def __init__(self, name, type, format, description, default, enum,
                 group, updatable, platforms, related_concepts, 
                 related_resources, links, choices, section):
        self.name = name
        self.type = type
        self.format = format
        self.description = description  # From CRD
        self.default = default
        self.enum = enum
        self.group = group  # From metadata
        self.updatable = updatable  # From metadata
        self.platforms = platforms  # From metadata
        self.related_concepts = related_concepts  # From metadata
        self.related_resources = related_resources  # From metadata
        self.links = links  # From metadata
        self.choices = choices  # Merged
        self.section = section
```

## Example: Complete Merge for linkAccess Property

### Input: CRD
```yaml
# From crds/skupper_site_crd.yaml
spec:
  properties:
    linkAccess:
      type: string
      description: |-
        Configure external access for links from remote sites. When
        set, implies a RouterAccess resource with accessType set
        according to the linkAccess value.

        Sites and links are the basis for creating application
        networks. In a simple two-site network, at least one of the
        sites must have link access enabled. Choices include:
        - `none`: No linking to this site is enabled.
        - `default`: Use the default link access for the current platform...
        - `route`: Use an OpenShift route.
        - `loadbalancer`: Use a Kubernetes load balancer.
      enum: [none, default, route, loadbalancer]
```

### Input: Metadata
```yaml
# From config/resources/metadata/site.yaml
properties:
  linkAccess:
    group: frequently-used
    updatable: true
    related_concepts: [link]
    links: [skupper/site-linking]
    choices:
      - name: none
        description: No linking to this site is permitted.
      - name: default
        platforms: [Kubernetes]
        description: |
          Use the default link access for the current platform.
          On OpenShift, the default is `route`. For other
          Kubernetes flavors, the default is `loadbalancer`.
      - name: route
        description: Use an OpenShift route. _OpenShift only._
      - name: loadbalancer
        description: Use a Kubernetes load balancer.
```

### Output: Merged Property Object
```python
Property(
    name="linkAccess",
    type="string",
    format=None,
    description="Configure external access for links from remote sites...",  # From CRD
    default=None,
    enum=["none", "default", "route", "loadbalancer"],  # From CRD
    group="frequently-used",  # From metadata
    updatable=True,  # From metadata
    platforms=[],  # From metadata (empty at property level)
    related_concepts=["link"],  # From metadata
    related_resources=[],  # From metadata
    links=["skupper/site-linking"],  # From metadata
    choices=[  # Merged from CRD enum + metadata descriptions
        {
            "name": "none",
            "description": "No linking to this site is permitted."
        },
        {
            "name": "default",
            "platforms": ["Kubernetes"],
            "description": "Use the default link access..."
        },
        {
            "name": "route",
            "description": "Use an OpenShift route. _OpenShift only._"
        },
        {
            "name": "loadbalancer",
            "description": "Use a Kubernetes load balancer."
        }
    ],
    section="spec"
)
```

### Output: Generated Markdown
```markdown
## Spec properties

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-link-access">linkAccess</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">frequently used</div>
</div>
<div class="attribute-body">

Configure external access for links from remote sites. When
set, implies a RouterAccess resource with accessType set
according to the linkAccess value.

Sites and links are the basis for creating application
networks. In a simple two-site network, at least one of the
sites must have link access enabled.

<table class="fields">
<tr><th>Choices</th><td>
<table class="choices">
<tr><th><code>none</code></th><td>
<p>No linking to this site is permitted.</p>
</td></tr>
<tr><th><code>default</code></th><td>
<p>Use the default link access for the current platform.
On OpenShift, the default is <code>route</code>. For other
Kubernetes flavors, the default is <code>loadbalancer</code>.</p>
<p><em>Kubernetes only</em></p>
</td></tr>
<tr><th><code>route</code></th><td>
<p>Use an OpenShift route. <em>OpenShift only.</em></p>
</td></tr>
<tr><th><code>loadbalancer</code></th><td>
<p>Use a Kubernetes load balancer.</p>
</td></tr>
</table>
</td></tr>
<tr><th>Updatable</th><td>True</td></tr>
<tr><th>See also</th><td>
<a href="/concepts/link.html">Link concept</a>,
<a href="/topics/site-linking.html">Site linking</a>
</td></tr>
</table>

</div>
</div>
```

## Benefits of This Approach

1. **Single Source for Descriptions**: CRD descriptions are authoritative
2. **Automatic Updates**: When CRD descriptions change, docs update automatically
3. **Minimal Metadata**: Only need to specify doc-specific info (grouping, links, etc.)
4. **No Duplication**: Don't repeat what's already in CRDs
5. **Clear Separation**: Technical schema (CRD) vs. documentation structure (metadata)
6. **Easy Maintenance**: Metadata files are ~80% smaller than current YAML configs

## Comparison: Current vs. New

### Current Approach (config/resources/site.yaml)
```yaml
# 161 lines total
name: Site
description: |
  A site is a place on the network where application workloads are
  running.  Sites are joined by [links](link.html).
  ...
spec:
  properties:
    - name: linkAccess
      group: frequently-used
      default: none
      updatable: true
      description: |
        Configure external access for links from remote sites.
        
        Sites and links are the basis for creating application
        networks.  In a simple two-site network, at least one of
        the sites must have link access enabled.
      choices:
        - name: none
          description: No linking to this site is permitted.
        # ... etc
```

### New Approach (config/resources/metadata/site.yaml)
```yaml
# ~99 lines total (38% reduction)
name: Site
examples:
  - description: A minimal site
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: Site
      ...
related_resources: [link]
properties:
  linkAccess:
    group: frequently-used
    updatable: true
    related_concepts: [link]
    choices:
      - name: none
        description: No linking to this site is permitted.
      # ... etc
```

**Key Difference**: Description comes from CRD, not duplicated in metadata.

## Migration Path

1. **Extract metadata** from current YAML configs (script provided in proposal)
2. **Remove descriptions** that are already in CRDs
3. **Keep only** doc-specific metadata (examples, grouping, links)
4. **Result**: Much smaller, cleaner metadata files

This gives you the best of both worlds: authoritative CRD descriptions with minimal documentation metadata.

## Validation and Warnings

The merge process includes comprehensive validation to catch mismatches:

### Enum/Choice Validation

When merging CRD enum values with metadata choice descriptions:

**Warning 1: Extra choices in metadata**
```
Site.linkAccess: Metadata defines choices not in CRD enum: {'custom', 'ingress'}
```
This means your metadata file has choice descriptions for values that don't exist in the CRD enum.

**Warning 2: Missing choices in metadata**
```
Site.linkAccess: CRD enum values lack metadata descriptions: {'nodeport'}
```
This means the CRD has enum values that don't have descriptions in your metadata file.

**Example Scenarios**:

#### Scenario 1: Perfect Match ✅
```yaml
# CRD
enum: [none, default, route, loadbalancer]

# Metadata
choices:
  - name: none
    description: ...
  - name: default
    description: ...
  - name: route
    description: ...
  - name: loadbalancer
    description: ...
```
**Result**: No warnings, all choices documented.

#### Scenario 2: Missing Metadata ⚠️
```yaml
# CRD
enum: [none, default, route, loadbalancer]

# Metadata
choices:
  - name: none
    description: ...
  - name: default
    description: ...
  # Missing: route, loadbalancer
```
**Result**: Warning about missing 'route' and 'loadbalancer' in metadata.
**Behavior**: Uses CRD description if available, otherwise no description shown.

#### Scenario 3: Extra Metadata ⚠️
```yaml
# CRD
enum: [none, default, route, loadbalancer]

# Metadata
choices:
  - name: none
    description: ...
  - name: default
    description: ...
  - name: route
    description: ...
  - name: loadbalancer
    description: ...
  - name: ingress  # Not in CRD!
    description: ...
```
**Result**: Warning about extra 'ingress' in metadata.
**Behavior**: Ignores the extra choice (not included in output).

### Property Validation

The existing validation (from `ResourceModel.check()`) continues to work:

**Warning 3: Missing properties**
```
Site: Spec property 'newField' is missing
```
CRD defines a property that doesn't have metadata.

**Warning 4: Extra properties**
```
Site: Spec property 'oldField' is extra
```
Metadata defines a property that doesn't exist in CRD.

### Validation Summary

| Check | When | Action |
|-------|------|--------|
| Extra enum in metadata | Choice in metadata not in CRD | Warn + Ignore |
| Missing enum in metadata | CRD enum lacks metadata | Warn + Use CRD description |
| Extra property in metadata | Property in metadata not in CRD | Warn |
| Missing property in metadata | CRD property lacks metadata | Warn |

### Running Validation

Validation runs automatically during generation:

```bash
$ ./plano generate
Generating resources
Site.linkAccess: CRD enum values lack metadata descriptions: {'nodeport'}
Connector.type: Metadata defines choices not in CRD enum: {'udp'}
Generated input/resources/site.md
Generated input/resources/connector.md
...
```

All warnings are non-fatal - generation continues but you're alerted to inconsistencies.
