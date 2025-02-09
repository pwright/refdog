---
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Listener concept
  url: /concepts/listener.html
- title: Listener resource
  url: /resources/listener.html
- title: Connector delete command
  url: /commands/connector/delete.html
- title: Connector command
  url: /commands/connector/index.html
refdog_object_has_attributes: true
---

# Listener delete command

~~~ shell
skupper listener delete <name> [options]
~~~

Delete a listener.

| Field       | Value |
|------------|-------|
| Platforms  | Kubernetes, Docker, Podman, Linux |
| Waits for  | Deletion |

.Examples

~~~ console
# Delete a listener
$ skupper listener delete database
Waiting for deletion...
Listener "database" is deleted.
~~~

.Primary options

&lt;name&gt;
required

The name of the resource to be deleted.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

--timeout

Raise an error if the operation does not complete in the given
period of time.

Default:: 60s

Platforms:: Kubernetes

--wait

Wait for deletion to complete before exiting.

Default:: true
Platforms:: Kubernetes

.Global options

--context
global

Set the kubeconfig context.

Platforms:: Kubernetes
See also: [Kubernetes kubeconfigs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

--kubeconfig
global

Set the path to the kubeconfig file.

Platforms:: Kubernetes
See also: [Kubernetes kubeconfigs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

--namespace
global

Set the current namespace.

See also: [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

--platform
global

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default:: kubernetes

Choices:: kubernetes:: Kubernetes

docker:: Docker

podman:: Podman

linux:: Linux

See also: [Platform concept]({{site_prefix}}/concepts/platform.html)

--help
global

Display help and exit.


