---
body_class: object command
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
refdog_object_has_attributes: true
---

# System command

~~~ shell
skupper system [subcommand] [options]
~~~

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Subcommands

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/system/install.html">System install</a></th><td>Checks the local environment for required resources and configuration</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/uninstall.html">System uninstall</a></th><td>Remove local system infrastructure, undoing the configuration changes made by skupper system install, by disabling the Podman/Docker API</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/start.html">System start</a></th><td>Start the Skupper router for the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/stop.html">System stop</a></th><td>Stop the Skupper router for the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/reload.html">System reload</a></th><td>Forces to overwrite an existing namespace based on input/resources, if the namespace is not provided, the default one is going to be reloaded
</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/apply.html">System apply</a></th><td>Create or update resources using files or standard input</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/delete.html">System delete</a></th><td>Delete resources using files or standard input</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/generate-bundle.html">System generate-bundle</a></th><td>Generate a self-contained site bundle for use on another machine</td></tr>
</table>
