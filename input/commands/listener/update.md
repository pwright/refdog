---
body_class: object command
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Listener concept
  url: /concepts/listener.html
- title: Listener resource
  url: /resources/listener.html
- title: Connector update command
  url: /commands/connector/update.html
- title: Connector command
  url: /commands/connector/index.html
refdog_object_has_attributes: true
---

# Listener update command

```shell
skupper listener update <name> [options]
```

Update a listener.

Platforms: Kubernetes, Docker, Podman, Linux
Waits for: Configured

## Examples

```console
# Change the host and port
$ skupper listener update database --host mysql --port 3306
Waiting for status...
Listener "database" is configured.

# Change the routing key
$ skupper listener update backend --routing-key be2
```

## Primary options

&lt;name&gt;
Type: string
Flags: required

The name of the resource to be updated.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/names/">Kubernetes object names</a></td></table>

--host
Type: <string>
Flags: frequently used

The hostname or IP address of the local listener.  Clients
at this site use the listener host and port to
establish connections to the remote service.

<table class="fields"><tr><th>Default</th><td><p><em>Value of name</em></p>
</td><tr><th>Updatable</th><td>True</td></table>

--port
Type: <integer>
Flags: frequently used

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

--wait
Type: <status>

Wait for the given status before exiting.

<table class="fields"><tr><th>Default</th><td><p><code>ready</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>none</code></th><td><p><em>Do not wait</em></p>
</td></tr><tr><th><code>configured</code></th><td><p>Configured</p>
</td></tr><tr><th><code>ready</code></th><td><p>Ready</p>
</td></tr></table></td><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/resource-status.html">Resource status</a></td></table>

--timeout
Type: <duration>

Raise an error if the operation does not complete in the given
period of time.

<table class="fields"><tr><th>Default</th><td><p><code>60s</code></p>
</td><tr><th>Platforms</th><td>Kubernetes</td></table>

## Global options

--context
Type: <name>
Flags: global

Set the kubeconfig context.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Kubernetes kubeconfigs</a></td></table>

--kubeconfig
Type: <file>
Flags: global

Set the path to the kubeconfig file.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Kubernetes kubeconfigs</a></td></table>

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


