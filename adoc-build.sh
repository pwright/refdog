./plano generate
bash adoc.sh
asciidoctor-reducer input/commands/commands.adoc > commands.adoc
asciidoctor-reducer input/concepts/concepts.adoc > concepts.adoc
asciidoctor-reducer input/resources/resources.adoc > resources.adoc
asciidoctor-reducer skupper.adoc > export.adoc
