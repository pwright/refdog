---
body_class: object command
refdog_links: []
refdog_object_has_attributes: true
---

# Version command

```shell
skupper version [options]
```

Display versions of Skupper components.

Platforms: Kubernetes, Docker, Podman, Linux

## Examples

```console
# Show component versions
$ skupper version
COMPONENT          VERSION
cli                2.0.0
controller         2.0.0
router             3.0.0

# Show version details in YAML format
$ skupper version --output yaml
components:
  cli:
    version: 2.0.0
  controller:
    version: 2.0.0
    images:
      controller:
        name: quay.io/skupper/controller:2.0.0
        digest: sha256:663d97f86ff3fcce27a3842cd2b3a8e32af791598a46d815c07b0aec07505f55
  router:
    version: 3.0.0
    images:
      router:
        name: quay.io/skupper/router:3.0.0
        digest: sha256:dc5e27385a1e110dd2db1903ba7ec3e0d50b57f742aa02d7dd0a7b1b68c34394
      kube-adaptor:
        name: quay.io/skupper/kube-adaptor:2.0.0
        digest: sha256:4dc24bb3d605ed3fcec2f8ef7d45ca883d9d87b278bfedd5fcca74281d617a5e
```

## Primary options

--output
Type: (-o) <format>

Produce verbose structured output.

<table class="fields"><tr><th>Choices</th><td><table class="choices"><tr><th><code>json</code></th><td><p>Produce JSON output</p>
</td></tr><tr><th><code>yaml</code></th><td><p>Produce YAML output</p>
</td></tr></table></td></table>

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


