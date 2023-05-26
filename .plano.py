from plano import *

import collections

@command
def generate():
    lines = list()

    def append(line=""):
        lines.append(line)

    data = read_yaml("resources.yaml")
    data = transform_data(data)

    append("- [Notes](#{})".format(get_fragment_id("notes")))
    append("- [Overview](#{})".format(get_fragment_id("overview")))

    for resource in data:
        if resource.get("hidden"):
            continue

        resource_name = resource["name"]
        resource_title = resource.get("title", resource_name)
        resource_diagram = f"images/{resource_name}.svg"

        append(f"- [{resource_title}](#{resource_name})")
        append("    - [Examples](#{})".format(get_fragment_id("examples")))

        for group in resource.get("groups", []):
            if group.get("hidden"):
                continue

            group_title = group["title"]
            group_id = make_resource_id(group_title)
            group_id = get_fragment_id(group_id)

            append(f"    - [{group_title}](#{group_id})")

    toc = "\n".join(lines)
    lines.clear()

    for resource in data:
        if resource.get("hidden"):
            continue

        resource_name = resource["name"]
        resource_title = resource.get("title", resource_name)
        resource_diagram = f"images/{resource_name}.svg"
        resource_description = resource.get("description", "").rstrip()

        append("## {}".format(resource_title))
        append()

        if resource_description:
            append(resource_description)
            append()

        if exists(resource_diagram):
            append(f"<img src=\"{resource_diagram}\" height=\"180\"/>")
            append()

        if "examples" in resource:
            append("### Examples")
            append()

            for example in resource["examples"]:
                example_title = example["title"]
                example_syntax = example.get("syntax", "")
                example_text = example["text"].rstrip()

                append(f"#### {example_title}")
                append()
                append(f"~~~ {example_syntax}")
                append(example_text)
                append("~~~")
                append()

        for group in resource.get("groups", []):
            if group.get("hidden"):
                continue

            group_title = group["title"]
            group_description = group.get("description", "").rstrip()
            group_id = make_resource_id(group_title)

            append(f"### {group_title}")
            append()

            if group_description:
                append(group_description)
                append()

            for option in group.get("options", []):
                if option.get("hidden"):
                    continue

                generate_option(lines, option)

    resources = "\n".join(lines)

    readme = read("README.md.in")
    readme = readme.replace("@toc@", toc)
    readme = readme.replace("@resources@", resources)

    write("README.md", readme)

def transform_data(data):
    for resource in data:
        if "extends" in resource:
            base_name = resource["extends"]

            for candidate in data:
                if candidate["name"] == base_name:
                    base = candidate
                    break
            else:
                raise Exception(f"I can't find base resource '{base_name}'")

            try:
                groups = resource["groups"]
            except KeyError:
                groups = dict()
                resource["groups"] = groups

            # Could use a nicer merge here

            try:
                base_groups = {x.name: x for x in base["groups"]}
            except KeyError:
                base_groups = None

            if "groups" in resource:
                for group in resource["groups"]:
                    if base_groups
                    if "groups" in base:
                        for base_group in base["groups"]:



                resource["groups"][0:0] = base["groups"]

    return data

def make_resource_id(title):
    return title.lower().replace(" ", "-")

fragment_ids = collections.defaultdict(int)

def get_fragment_id(fragment_id):
    count = fragment_ids[fragment_id]
    fragment_ids[fragment_id] += 1

    if count == 0:
        return fragment_id
    else:
        return f"{fragment_id}-{count}"

def generate_option(lines, option):
    name = option["name"].strip()
    description = option.get("description", "").strip()
    type_ = capitalize(option.get("type", ""))

    # XXX Minor hack
    if type_ == "Boolean" and "default" not in option:
        option["default"] = False

    default = str(option.get("default", "")).strip()
    choices = option.get("choices")

    lines.append(f"* **`{name}`**")
    lines.append("")

    if "description" in option:
        lines.append(f"  {description}".replace("\n", "\n  "))

    lines.append("  ")

    if "type" in option:
        lines.append(f"  _Type_: {type_}\\")

    if "default" in option:
        if type_ in ("String", "Duration") and default != "*Generated*" and " " not in default:
            default = f"`{default}`"

        lines.append(f"  _Default_: {default}\\")
    elif "choices" in option:
        lines.append(f"  _Default_: `{choices[0]}`\\")

    if "choices" in option:
        choices = ", ".join([f"`{x}`" for x in choices])
        lines.append(f"  _Choices_: {choices}\\")

    # Chomp off the last backslash
    lines[-1] = lines[-1].removesuffix("\\")

    lines.append("")

render_template = """
<html>
  <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown.min.css"
          integrity="sha512-KUoB3bZ1XRBYj1QcH4BHCQjurAZnCO3WdrswyLDtp7BMwCw7dPZngSLqILf68SGgvnWHTD5pPaYrXi6wiRJ65g=="
          crossorigin="anonymous" referrerpolicy="no-referrer"/>
    <style>
        .markdown-body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }
        @media (max-width: 767px) {
           .markdown-body {
               padding: 15px;
           }
        }
    </style>
  </head>
  <body>
    <article class="markdown-body">
@content@
    </article>
  </body>
</html>
""".strip()

@command
def render():
    """
    Render README.html from the data in skewer.yaml
    """
    generate()

    markdown = read("README.md")
    data = {"text": markdown}
    json = emit_json(data)
    content = http_post("https://api.github.com/markdown", json, content_type="application/json")
    html = render_template.replace("@content@", content)

    write("README.html", html)

    print(f"file:{get_real_path('README.html')}")

@command
def clean():
    remove("README.html")
    remove(find(".", "__pycache__"))
