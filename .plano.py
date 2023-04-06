from plano import *

entry = """    - name: {name}
      default:
      required: n
      type: {type}
      description: |
        {description}"""

@command
def convert_help():
    for line in STDIN:
        line = line.strip()

        if not line:
            continue

        if not line.startswith("--"):
            continue

        elems = line.split()
        name = elems[0][2:]

        if elems[1] in ("int", "string", "strings", "duration"):
            type = elems[1]
            description = " ".join(elems[2:])
        else:
            type = bool
            description = " ".join(elems[1:])

        print(entry.format(**locals()))

@command
def generate():
    out = list()
    data = read_yaml("resources.yaml")

    out.append("# Refdog")
    out.append("")

    for resource in data:
        out.append("- [Resource _{}_](#resource-{})".format(resource["name"], resource["name"]))

        for group in resource.get("groups", []):
            out.append("    - [{}](#{})".format(group["title"], group["title"].lower().replace(" ", "-")))

    out.append("")

    for resource in data:
        out.append("## Resource _{}_".format(resource["name"]))
        out.append("")

        out.append("<dl>")

        for entry in resource.get("entries", []):
            generate_entry(out, entry)

        out.append("</dl>")
        out.append("")

        for group in resource.get("groups", []):
            out.append("### {}".format(group["title"]))
            out.append("")

            out.append("<dl>")

            for entry in group.get("entries", []):
                generate_entry(out, entry)

            out.append("</dl>")
            out.append("")

    write("README.md", "\n".join(out))

def generate_entry(out, entry):
    out.append("<dt><p>{}</p></dt>".format(entry["name"]))
    out.append("<dd>")
    out.append("<p>{}</p>".format(entry["description"]).strip())

    out.append("<div><b>Type:</b> {}</div>".format(capitalize(entry["type"])))

    if "default" in entry and entry["default"] is not None:
        out.append("<div><b>Default:</b> {}</div>".format(entry["default"]))

    if "choices" in entry:
        out.append("<div><b>Choices:</b> {}</div>".format(", ".join(entry["choices"])))

    out.append("</dd>")

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
