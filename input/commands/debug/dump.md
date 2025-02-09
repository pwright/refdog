---
refdog_links:
- title: Debug dumps
  url: /topics/debug-dumps.html
refdog_object_has_attributes: true
---

# Debug dump command

~~~ shell
skupper debug dump [file] [options]
~~~

Generate a debug dump file.  Debug dumps collect the details of
a site so another party can identify and fix a problem.

| Field       | Value |
|------------|-------|
| Platforms  | Kubernetes, Docker, Podman, Linux |

.Examples

~~~ console
# Generate a dump file
$ skupper debug dump
Debug dump file: /home/fritz/skupper-dump-west-2024-12-09.tar.gz

# Generate a dump file to a particular path
$ skupper debug dump /tmp/abc.tar.gz
Debug dump file: /tmp/abc.tar.gz
~~~

.Primary options

[file]
optional

The name of the file to generate.

The command exits with an error if the file already exists.

Default:: <code>skupper-dump-&lt;site-name&gt;-&lt;date&gt;.tar.gz</code>


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


