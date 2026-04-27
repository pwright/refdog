---
body_class: object command
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Link concept
  url: /concepts/link.html
- title: Link resource
  url: /resources/link.html
- title: Token command
  url: /commands/token/index.html
refdog_object_has_attributes: true
---

# Link command

~~~ shell
skupper link [subcommand] [options]
~~~

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Subcommands

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/link/update.html">Link update</a></th><td>Change link settings
</td></tr>
<tr><th><a href="{{site.prefix}}/commands/link/delete.html">Link delete</a></th><td>Delete a link by name
</td></tr>
<tr><th><a href="{{site.prefix}}/commands/link/status.html">Link status</a></th><td>Display the status of links in the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/link/generate.html">Link generate</a></th><td>Generate a new link resource as a YAML output, unless explicitly specified otherwise using the --output flag</td></tr>
</table>
