---
refdog_links: []
refdog_object_has_attributes: true
---

# Debug check command

```shell
skupper debug check [options]
```

Run diagnostic checks.

Platforms: Kubernetes, Docker, Podman, Linux

## Primary options

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


