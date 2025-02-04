---
body_class: object command
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: System install command
  url: /commands/system/install.html
refdog_object_has_attributes: true
---

# System uninstall command

```shell
skupper system uninstall [options]
```

Remove local system infrastructure.

This operation fails if sites are present.  Use the
`--force` option to override.

Platforms: Kubernetes, Docker, Podman, Linux

## Primary options

--force
Type: boolean



## Global options

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


