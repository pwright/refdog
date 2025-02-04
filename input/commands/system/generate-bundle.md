---
body_class: object command
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
refdog_object_has_attributes: true
---

# System generate-bundle command

```shell
skupper system generate-bundle <bundle-file> [options]
```

Generate a self-contained site bundle for use on another
machine.

Platforms: Kubernetes, Docker, Podman, Linux

## Primary options

&lt;bundle-file&gt;
Type: string
Flags: required

The name of the bundle file to generate.

The command exits with an error if the file already exists.



--input
Type: <string>

The location of the Skupper resources defining the site.

<table class="fields"><tr><th>Default</th><td><p><code>$HOME/.local/share/skupper/namespaces/&lt;namespace&gt;/input/resources</code></p>
</td></table>

--type
Type: <string>

<table class="fields"><tr><th>Default</th><td><p><code>tarball</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>tarball</code></th><td><p>A gzipped tar file</p>
</td></tr><tr><th><code>shell-script</code></th><td><p>A self-extracting shell script</p>
</td></tr></table></td></table>

## Global options

--namespace
Type: (-n) <name>
Flags: global

Set the current namespace.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/">Kubernetes namespaces</a>, <a href="{{site_prefix}}/topics/system-namespaces.html">System namespaces</a></td></table>

--platform
Type: <platform>
Flags: global

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

<table class="fields"><tr><th>Default</th><td><p><code>kubernetes</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>kubernetes</code></th><td><p>Kubernetes</p>
</td></tr><tr><th><code>docker</code></th><td><p>Docker</p>
</td></tr><tr><th><code>podman</code></th><td><p>Podman</p>
</td></tr><tr><th><code>linux</code></th><td><p>Linux</p>
</td></tr></table></td><tr><th>See also</th><td><a href="{{site_prefix}}/concepts/platform.html">Platform concept</a></td></table>

--help
Type: (-h) boolean
Flags: global

Display help and exit.


