---
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Connector concept
  url: /concepts/connector.html
- title: Connector resource
  url: /resources/connector.html
- title: Listener update command
  url: /commands/listener/update.html
- title: Listener command
  url: /commands/listener/index.html
refdog_object_has_attributes: true
---

# Connector update command

```shell
skupper connector update <name> <port> [options]
```

Update a connector.

Platforms: Kubernetes, Docker, Podman, Linux
Waits for: Configured

## Examples

```console
# Change the workload and port
$ skupper connector update database --workload deployment/mysql --port 3306
Waiting for status...
Connector "database" is configured.

# Change the routing key
$ skupper connector update backend --routing-key be2
```

## Primary options

&lt;name&gt;
Type: string
Flags:: required

The name of the resource to be updated.

See also: Kubernetes object names (https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

&lt;port&gt;
Type: integer
Flags:: required

The port on the target server to connect to.

Updatable: True

--routing-key
Type: <string>
Flags:: frequently used

The identifier used to route traffic from listeners to
connectors.  To expose a local workload to a remote site, the
remote listener and the local connector must have matching
routing keys.

Default: <p><em>Value of name</em></p>

Updatable: True

--workload
Type: <resource>
Flags:: frequently used

A Kubernetes resource name that identifies a workload.  It uses
`<resource-type>/<resource-name>` syntax and resolves to an
equivalent pod selector.

This is an alternative to setting the `--selector` or
`--host` options.

Platforms: Kubernetes
See also: Kubernetes workloads (https://kubernetes.io/docs/concepts/workloads/)

--selector
Type: <string>

A Kubernetes label selector for specifying target server pods.  It
uses `<label-name>=<label-value>` syntax.

This is an alternative to setting the `--workload` or
`--host` options.

Default: <p>app=[value-of-name]</p>

Platforms: Kubernetes
Updatable: True
See also: Kubernetes label selectors (https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors)

--host
Type: <string>

The hostname or IP address of the server.  This is an
alternative to `selector` for specifying the target server.

This is an alternative to setting the `--selector` or
`--workload` options.

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


