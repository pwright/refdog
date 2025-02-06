---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
refdog_object_has_attributes: true
---

# System generate-bundle command

~~~ shell
skupper system generate-bundle <bundle-file> [options]
~~~

Generate a self-contained site bundle for use on another
machine.

| Field       | Value |
|------------|-------|
| Platforms  | Kubernetes, Docker, Podman, Linux |

.Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-bundle-file">&lt;bundle-file&gt;</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The name of the bundle file to generate.

The command exits with an error if the file already exists.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-input">--input</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

The location of the Skupper resources defining the site.

Default:: $HOME/.local/share/skupper/namespaces/<namespace>/input/resources


</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-type">--type</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

Default:: tarball

Choices:: tarball:: A gzipped tar file

shell-script:: A self-extracting shell script


</div>
</div>

.Global options

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-namespace">--namespace</h3>
<div class="attribute-type-info">(-n) &lt;name&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the current namespace.

See also: [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-platform">--platform</h3>
<div class="attribute-type-info">&lt;platform&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default:: kubernetes

Choices:: kubernetes:: Kubernetes

docker:: Docker

podman:: Podman

linux:: Linux

See also: [Platform concept]({{site_prefix}}/concepts/platform.html)

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">(-h) boolean</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Display help and exit.



</div>
</div>
