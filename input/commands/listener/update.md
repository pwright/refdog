---
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
Flags:: required

The name of the resource to be updated.

See also: Kubernetes object names (https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

--host
Type: <string>
Flags:: frequently used

The hostname or IP address of the local listener.  Clients
at this site use the listener host and port to
establish connections to the remote service.

Default: <p><em>Value of name</em></p>

Updatable: True

--port
Type: <integer>
Flags:: frequently used

The port of the local listener.  Clients at this site use
the listener host and port to establish connections to
the remote service.

Updatable: True

--routing-key
Type: <string>
Flags:: frequently used

The identifier used to route traffic from listeners to
connectors.  To enable connecting to a service at a
remote site, the local listener and the remote connector
must have matching routing keys.

Default: <p><em>Value of name</em></p>

Updatable: True

--wait
Type: <status>

Wait for the given status before exiting.

Default: <p>ready</p>

Choices: none: <p><em>Do not wait</em></p>

configured: <p>Configured</p>

ready: <p>Ready</p>

Platforms: Kubernetes
See also: Resource status ({{site_prefix}}/topics/resource-status.html)

--timeout
Type: <duration>

Raise an error if the operation does not complete in the given
period of time.

Default: <p>60s</p>

Platforms: Kubernetes

## Global options

--context
Type: <name>
Flags:: global

Set the kubeconfig context.

Platforms: Kubernetes
See also: Kubernetes kubeconfigs (https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

--kubeconfig
Type: <file>
Flags:: global

Set the path to the kubeconfig file.

Platforms: Kubernetes
See also: Kubernetes kubeconfigs (https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

--namespace
Type: (-n) <name>
Flags:: global

Set the current namespace.

See also: Kubernetes namespaces (https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), System namespaces ({{site_prefix}}/topics/system-namespaces.html)

--platform
Type: <platform>
Flags:: global

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default: <p>kubernetes</p>

Choices: kubernetes: <p>Kubernetes</p>

docker: <p>Docker</p>

podman: <p>Podman</p>

linux: <p>Linux</p>

See also: Platform concept ({{site_prefix}}/concepts/platform.html)

--help
Type: (-h) boolean
Flags:: global

Display help and exit.


