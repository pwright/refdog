---
refdog_links:
- title: Debug dumps
  url: /topics/debug-dumps.html
refdog_object_has_attributes: true
---

# Debug dump command

```shell
skupper debug dump [file] [options]
```

Generate a debug dump file.  Debug dumps collect the details of
a site so another party can identify and fix a problem.

Platforms: Kubernetes, Docker, Podman, Linux

## Examples

```console
# Generate a dump file
$ skupper debug dump
Debug dump file: /home/fritz/skupper-dump-west-2024-12-09.tar.gz

# Generate a dump file to a particular path
$ skupper debug dump /tmp/abc.tar.gz
Debug dump file: /tmp/abc.tar.gz
```

## Primary options

[file]
Type: string
Flags:: optional

The name of the file to generate.

The command exits with an error if the file already exists.

Default: <p><code>skupper-dump-&lt;site-name&gt;-&lt;date&gt;.tar.gz</code></p>


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


