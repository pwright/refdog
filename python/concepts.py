from common import *

def generate(model):
    notice("Generating concepts")
    
    

    make_dir("input/concepts")
        # AsciiDoc output
    append_adoc = StringBuilder()
    append_adoc("== Skupper concepts")
    append_adoc()

    append = StringBuilder()

    append("---")
    append("refdog_links:")
    append("  - title: Concept overview")
    append("    url: overview.html")
    append("  - title: Resource index")
    append("    url: /resources/index.html")
    append("  - title: Command index")
    append("    url: /commands/index.html")
    append("---")
    append()
    append("# Skupper concepts")
    append()

    for group in model.groups:
        append(f"#### {group.title}")
        append()
        append("<table class=\"objects\">")

        for concept in group.objects:
            append(f"<tr><th><a href=\"{concept.href}\">{concept.title}</a></th><td>{concept.summary}</td></tr>")
            #append_adoc(f"== {concept.title}\n\n{concept.summary}\n")
            adoc_href = concept.href.replace(".html", ".adoc").replace("{{site_prefix}}/concepts/", "")
            append_adoc(f"include::{adoc_href}[leveloffset=+1]")
            append_adoc()


        append("</table>")
        append()

    append.write("input/concepts/index.md")
    
    append_adoc.write("input/concepts/concepts.adoc")
    

    for concept in model.concepts:
        generate_concept(concept)

def generate_concept(concept):
    notice(f"Generating {concept.input_file}")

    append = StringBuilder()

    append("---")
    append(generate_object_metadata(concept))
    append("---")
    append()
    append(f"# {concept.title_with_type}")
    append()

    if concept.description:
        append(concept.description.strip())
        append()

    append.write(concept.input_file)

class ConceptModel(Model):
    def __init__(self):
        super().__init__(Concept, "config/concepts")

        self.init()

    @property
    def concepts(self):
        return self.objects

class Concept(ModelObject):
    pass
