---
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Connector concept
  url: /concepts/connector.html
- title: Connector resource
  url: /resources/connector.html
- title: Listener delete command
  url: /commands/listener/delete.html
- title: Listener command
  url: /commands/listener/index.html
refdog_object_has_attributes: true
---

# Connector delete command

```shell
skupper connector delete <name> [options]
```

Delete a connector.

Platforms: Kubernetes, Docker, Podman, Linux
Waits for: Deletion

## Examples

```console
# Delete a connector
$ skupper connector delete database
Waiting for deletion...
Connector "database" is deleted.
```

## Primary options

&lt;name&gt;
Type: string
Flags:: required

The name of the resource to be deleted.

See also: Kubernetes object names (https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

--timeout
Type: <duration>

Raise an error if the operation does not complete in the given
period of time.

Default: <p>60s</p>

Platforms: Kubernetes

--wait
Type: boolean

Wait for deletion to complete before exiting.

Default: true
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


