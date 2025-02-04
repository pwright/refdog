---
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
Flags:: required

The name of the resource to be created.


The name is the default routing key and host if the
`--routing-key` and `--host` options are not specified.

See also: Kubernetes object names (https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

&lt;port&gt;
Type: integer
Flags:: required

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

--host
Type: <string>
Flags:: frequently used

The hostname or IP address of the local listener.  Clients
at this site use the listener host and port to
establish connections to the remote service.

Default: <p><em>Value of name</em></p>

Updatable: True

--wait
Type: <status>

Wait for the given status before exiting.

Default: <p>ready</p>

Choices: none: <p>Do not wait.</p>

configured: <p>Wait until the configuration is applied.</p>

ready: <p>Wait until the resource is ready to use.</p>

Platforms: Kubernetes
See also: Resource status ({{site_prefix}}/topics/resource-status.html)

--timeout
Type: <duration>

Raise an error if the operation does not complete in the given
period of time.

Default: <p>60s</p>

Platforms: Kubernetes
See also: Duration format (https://pkg.go.dev/time#ParseDuration)

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


