---
body_class: object command
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Listener concept
  url: /concepts/listener.html
- title: Listener resource
  url: /resources/listener.html
- title: Connector create command
  url: /commands/connector/create.html
- title: Connector command
  url: /commands/connector/index.html
refdog_object_has_attributes: true
---

# Listener create command

```shell
skupper listener create <name> <port> [options]
```

Create a listener.

Platforms: Kubernetes, Docker, Podman, Linux
Waits for: Configured

## Examples

```console
# Create a listener for a database
$ skupper listener create database 5432
Waiting for status...
Listener "database" is configured.

# Set the routing key and host explicitly
$ skupper listener create backend 8080 --routing-key be1 --host apiserver
```

## Primary options

&lt;name&gt;
Type: string
Flags: required

The name of the resource to be created.


The name is the default routing key and host if the
`--routing-key` and `--host` options are not specified.

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

<table class="fields"><tr><th>Default</th><td><p><code>ready</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>none</code></th><td><p>Do not wait.</p>
</td></tr><tr><th><code>configured</code></th><td><p>Wait until the configuration is applied.</p>
</td></tr><tr><th><code>ready</code></th><td><p>Wait until the resource is ready to use.</p>
</td></tr></table></td><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/resource-status.html">Resource status</a></td></table>

--timeout
Type: <duration>

Raise an error if the operation does not complete in the given
period of time.

<table class="fields"><tr><th>Default</th><td><p><code>60s</code></p>
</td><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="https://pkg.go.dev/time#ParseDuration">Duration format</a></td></table>

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


