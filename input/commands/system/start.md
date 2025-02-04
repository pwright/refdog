---
body_class: object command
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: System stop command
  url: /commands/system/stop.html
refdog_object_has_attributes: true
---

# System start command

```shell
skupper system start [options]
```

Start the Skupper router for the current site.  This starts the
systemd service for the current namespace.

**Note:** In the absence of a long-lived controller, this
operation first reads the input resources and updates the router
configuration.  With a long-lived controller, that config update
would have already taken place.

Platforms: Kubernetes, Docker, Podman, Linux

## Primary options

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


