---
body_class: object command
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Listener concept
  url: /concepts/listener.html
- title: Listener resource
  url: /resources/listener.html
- title: Connector generate command
  url: /commands/connector/generate.html
- title: Connector command
  url: /commands/connector/index.html
refdog_object_has_attributes: true
---

# Listener generate command

```shell
skupper listener generate <name> <port> [options]
```

Generate a Listener resource.

Platforms: Kubernetes, Docker, Podman, Linux

## Examples

```console
# Generate a Listener resource and print it to the console
$ skupper listener generate backend 8080
apiVersion: skupper.io/v2alpha1
kind: Listener
metadata:
  name: backend
spec:
  routingKey: backend
  port: 8080
  host: backend

# Generate a Listener resource and direct the output to a file
$ skupper listener generate backend 8080 > backend.yaml
```

## Primary options

&lt;name&gt;
Type: string
Flags: required

The name of the resource to be generated.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/names/">Kubernetes object names</a></td></table>

&lt;port&gt;
Type: integer
Flags: required

The port of the local listener.  Clients at this site use
the listener host and port to establish connections to
the remote service.

<table class="fields"><tr><th>Updatable</th><td>True</td></table>

--routing-key
Type: <string>
Flags: frequently used

The identifier used to route traffic from listeners to
connectors.  To enable connecting to a service at a
remote site, the local listener and the remote connector
must have matching routing keys.

<table class="fields"><tr><th>Default</th><td><p><em>Value of name</em></p>
</td><tr><th>Updatable</th><td>True</td></table>

--host
Type: <string>
Flags: frequently used

The hostname or IP address of the local listener.  Clients
at this site use the listener host and port to
establish connections to the remote service.

<table class="fields"><tr><th>Default</th><td><p><em>Value of name</em></p>
</td><tr><th>Updatable</th><td>True</td></table>

--wait
Type: <status>

Wait for the given status before exiting.

<table class="fields"><tr><th>Default</th><td><p><code>configured</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>none</code></th><td><p><em>Do not wait</em></p>
</td></tr><tr><th><code>configured</code></th><td><p>Configured</p>
</td></tr><tr><th><code>ready</code></th><td><p>Ready</p>
</td></tr></table></td></table>

--output
Type: (-o) <format>

Select the output format.

<table class="fields"><tr><th>Default</th><td><p><code>yaml</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>json</code></th><td><p>Produce JSON output</p>
</td></tr><tr><th><code>yaml</code></th><td><p>Produce YAML output</p>
</td></tr></table></td></table>

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


