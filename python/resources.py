from common import *

import fnmatch

def generate(model):
    debug("Generating resources")

    make_dir("input/resources")

    lines = list()

    def append(line=""):
        if line is None:
            return

        lines.append(line)

    append("---")
    append("links:")
    append("  - name: Skupper concepts")
    append("    url: /concepts/index.html")
    append("  - name: Skupper commands")
    append("    url: /commands/index.html")
    append("---")
    append()
    append("# Skupper resources")
    append()

    append("## Key resources")
    append()
    append("")
    append()
    append("## All resources")
    append()

    for group in model.groups:
        append(f"#### {group.name}")
        append()
        append("<table class=\"objects\">")

        for resource in group.resources:
            title = resource.title.removesuffix(" resource")
            description = nvl(resource.description, "").replace("\n", " ")
            description = description.split(".")[0]
            description = mistune.html(description)

            append(f"<tr><th><a href=\"{resource.href}\">{title}</a></th><td>{description}</td></tr>")

        append("</table>")
        append()

    write("input/resources/index.md", "\n".join(lines))

    for resource in model.resources:
        generate_resource(resource)

def generate_resource(resource):
    debug(f"Generating {resource}")

    if resource.hidden:
        debug(f"{resource} is hidden")
        return

    lines = list()

    def append(line=""):
        if line is None:
            return

        lines.append(line)

    append("---")
    append("body_class: object resource")
    append(generate_object_links(resource))
    append("---")
    append()
    append(f"# {capitalize(resource.rename)} resource")
    append()
    append("<section>")
    append()

    if resource.description:
        append(resource.description.strip())
        append()

    append("~~~ yaml")
    append("apiVersion: skupper.io/v2alpha1")
    append(f"kind: {resource.rename}")
    append("~~~")

    append()
    append("</section>")
    append()

    if resource.examples:
        append("<section>")
        append()
        append("## Examples")
        append()

        for example in resource.examples:
            append(example["description"].strip() + ":")
            append()
            append("~~~ yaml")
            append(example["yaml"].strip())
            append("~~~")
            append()

        append("</section>")
        append()

    append("<section class=\"attributes\">")
    append()
    append("## Metadata properties")
    append()

    for prop in resource.metadata_properties:
        generate_property(prop, append)

    append("</section>")
    append()
    append("<section class=\"attributes\">")
    append()
    append("## Spec properties")
    append()

    for group in ("required", "frequently-used", None, "advanced", "global"):
        for prop in resource.spec_properties:
            if prop.group == group:
                generate_property(prop, append)

    append("</section>")
    append()
    append("<section class=\"attributes\">")
    append()
    append("## Status properties")
    append()

    for group in ("required", "frequently-used", None, "advanced", "global"):
        for prop in resource.status_properties:
            if prop.group == group:
                generate_property(prop, append)

    append("</section>")
    append()

    if resource.notes:
        append("<section class=\"notes\">")
        append()
        append("## Notes")
        append()
        append(resource.notes.strip())
        append()
        append("</section>")
        append()

    write(f"input/resources/{resource.id}.md", "\n".join(lines))

def generate_property(prop, append):
    debug(f"Generating {prop}")

    if prop.hidden:
        debug(f"{prop} is hidden")
        return

    classes = ["attribute"]
    flags = list()
    name = nvl(prop.rename, prop.name)
    id_ = f"{prop.section}-{get_fragment_id(name)}"

    if prop.format:
        type_info = f"{prop.type} ({prop.format})"
    else:
        type_info = prop.type

    if prop.group:
        flags.append(prop.group.replace("-", " "))

    if prop.group not in ("required", "frequently-used"):
        classes.append("folded")

    append(f"<div class=\"{' '.join(classes)}\">")
    append(f"<div class=\"attribute-heading\">")
    append(f"<h3 id=\"{id_}\">{name}</h3>")
    append(f"<div class=\"attribute-type-info\">{type_info}</div>")

    if flags:
        append(f"<div class=\"attribute-flags\">{', '.join(flags)}</div>")

    append("</div>")
    append("<div class=\"attribute-body\">")
    append()

    if prop.description:
        append(prop.description.strip())
        append()

    append(generate_attribute_fields(prop))
    append()

    if prop.notes:
        append("<section class=\"notes\">")
        append()
        append(prop.notes.strip())
        append()
        append("</section>")
        append()

    append("</div>")
    append("</div>")
    append()

class ResourceModel:
    def __init__(self):
        debug(f"Loading {self}")

        self.data = read_yaml("config/resources.yaml")

        self.resources = list()
        self.resources_by_name = dict()
        self.groups = list()
        self.crds_by_name = dict()

        for resource_data in self.data["resources"]:
            resource = Resource(self, resource_data)

            self.resources.append(resource)
            self.resources_by_name[resource.name] = resource

        for group_data in self.data["groups"]:
            self.groups.append(ResourceGroup(self, group_data))

        with working_dir("crds"):
            for crd_file in list_dir():
                if crd_file == "skupper_cluster_policy_crd.yaml":
                    continue

                crd_data = read_yaml(crd_file)

                if crd_data["kind"] != "CustomResourceDefinition":
                    continue

                kind = crd_data["spec"]["names"]["kind"]

                self.crds_by_name[kind] = crd_data

    def __repr__(self):
        return self.__class__.__name__

    def check(self):
        for crd_name, crd_data in self.crds_by_name.items():
            try:
                resource = self.resources_by_name[crd_name]
            except KeyError:
                warning(f"Resource '{crd_name}' is missing")
                continue

            for name, data in crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"].items():
                if name not in resource.spec_properties_by_name:
                    warning(f"{resource}: Spec property '{name}' is missing")

            for name, data in crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["status"]["properties"].items():
                if name not in resource.status_properties_by_name:
                    warning(f"{resource}: Status property '{name}' is missing")

        for resource in self.resources:
            try:
                crd_data = self.crds_by_name[resource.name]
            except KeyError:
                warning(f"Resource '{resource.name}' is extra")
                continue

            for prop in resource.spec_properties:
                if prop.name not in crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["spec"]["properties"]:
                    warning(f"{resource}: Spec property '{prop.name}' is extra")

            for prop in resource.status_properties:
                if prop.name not in crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["status"]["properties"]:
                    warning(f"{resource}: Status property '{prop.name}' is extra")

    def get_schema(self, resource):
        try:
            return self.crds_by_name[resource.name]["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
        except KeyError:
            return {}

    def get_schema_property(self, prop):
        if prop.object is None:
            return {}

        schema = self.get_schema(prop.object)

        try:
            return schema["properties"][prop.section]["properties"][prop.name]
        except KeyError:
            return {}

class Resource(ModelObject):
    examples = object_property("examples", default=[])
    description = object_property("description")

    def __init__(self, model, data):
        super().__init__(model, data)

        self.metadata_properties = list()
        self.metadata_properties_by_name = dict()

        if "metadata" in self.data:
            for data in self.merge_property_data("metadata"):
                prop = Property(self.model, self, data, "metadata")

                self.metadata_properties.append(prop)
                self.metadata_properties_by_name[prop.name] = prop

        self.spec_properties = list()
        self.spec_properties_by_name = dict()

        if "spec" in self.data:
            for data in self.merge_property_data("spec"):
                prop = Property(self.model, self, data, "spec")

                self.spec_properties.append(prop)
                self.spec_properties_by_name[prop.name] = prop

        self.status_properties = list()
        self.status_properties_by_name = dict()

        if "status" in self.data:
            for data in self.merge_property_data("status"):
                prop = Property(self.model, self, data, "status")

                self.status_properties.append(prop)
                self.status_properties_by_name[prop.name] = prop

    def merge_property_data(self, section):
        model_props = self.model.data.get("properties", {})
        included_keys = list()

        for pattern in self.data[section].get("include_properties", []):
            for key in model_props:
                if fnmatch.fnmatchcase(key, pattern):
                    included_keys.append(key)

        for pattern in self.data[section].get("exclude_properties", []):
            for key in included_keys:
                if fnmatch.fnmatchcase(key, pattern):
                    included_keys.remove(key)

        included_props = {model_props[x]["name"]: model_props[x] for x in included_keys}
        specific_props = {x["name"]: x for x in self.data[section].get("properties", [])}

        included_names = [x for x in included_props if x not in specific_props]
        merged_names = list(specific_props.keys()) + included_names
        merged_props = list()

        for name in merged_names:
            included_data = included_props.get(name, {})
            specific_data = specific_props.get(name, {})

            merged_data = dict(included_data)
            merged_data.update(specific_data)

            if "description" in included_data and "description" in specific_data:
                included_description = included_data["description"]
                specific_description = specific_data["description"]

                merged_data["description"] = specific_description.replace("@description@", included_description)

            merged_props.append(merged_data)

        return merged_props

class ResourceGroup(ModelObjectGroup):
    def __init__(self, model, data):
        super().__init__(model, data)

        self.resources = list()

        for resource_name in self.data.get("resources", []):
            self.resources.append(self.model.resources_by_name[resource_name])

def property_property(name):
    def get(obj):
        # XXX if prop.section in ("spec", "status"):
        default = obj.model.get_schema_property(obj).get(name)
        return obj.data.get(name, default)

    return property(get)

class Property(ModelObjectAttribute):
    type = property_property("type")
    format = property_property("format")
    description = property_property("description")

    def __init__(self, model, resource, data, section):
        super().__init__(model, resource, data)

        self.resource = resource
        self.section = section

    @property
    def required(self):
        default = None

        if self.section in ("spec", "status"):
            schema = self.model.get_schema(self.object)
            required_names = schema["properties"][self.section].get("required", [])
            default = self.name in required_names

        return self.data.get("required", default)

    @property
    def default(self):
        default = False if self.type == "boolean" else None
        return self.data.get("default", default)

    @property
    def choices(self):
        default = self.model.get_schema_property(self).get("enum")
        return self.data.get("choices", [])
