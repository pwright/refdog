---
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Link concept
  url: /concepts/link.html
- title: Link resource
  url: /resources/link.html
- title: Token command
  url: /commands/token/index.html
refdog_object_has_attributes: true
---

# Link update command

```shell
skupper link update <name> [options]
```

Change link settings.

Platforms:: Kubernetes, Docker, Podman, Linux

Waits for:: Ready


.Examples

```console
# Change the link cost
$ skupper link update west-6bfn6 --cost 10
Waiting for status...
Link "west-6bfn6" is ready.
```

.Primary options

---
**&lt;name&gt;**

Type:: string

Flags:: required


The name of the resource to be updated.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

---
**--cost**

Type:: <integer>


The configured routing cost of sending traffic over
the link.

Default:: 1
See also: [Load balancing]({{site_prefix}}/topics/load-balancing.html)

---
**--timeout**

Type:: <duration>


Raise an error if the operation does not complete in the given
period of time.

Default:: 60s

Platforms:: Kubernetes

---
**--wait**

Type:: <status>


Wait for the given status before exiting.

Default:: ready

Choices:: none:: <em>Do not wait</em>

configured:: Configured

ready:: Ready

Platforms:: Kubernetes
See also: [Resource status]({{site_prefix}}/topics/resource-status.html)

.Global options

---
**--context**

Type:: <name>

Flags:: global


Set the kubeconfig context.

Platforms:: Kubernetes
See also: [Kubernetes kubeconfigs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

---
**--kubeconfig**

Type:: <file>

Flags:: global


Set the path to the kubeconfig file.

Platforms:: Kubernetes
See also: [Kubernetes kubeconfigs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

---
**--namespace**

Type:: (-n) <name>

Flags:: global


Set the current namespace.

See also: [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

---
**--platform**

Type:: <platform>

Flags:: global


Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default:: kubernetes

Choices:: kubernetes:: Kubernetes

docker:: Docker

podman:: Podman

linux:: Linux

See also: [Platform concept]({{site_prefix}}/concepts/platform.html)

---
**--help**

Type:: (-h) boolean

Flags:: global


Display help and exit.


