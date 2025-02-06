---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: System install command
  url: /commands/system/install.html
refdog_object_has_attributes: true
---

# System uninstall command

~~~ shell
skupper system uninstall [options]
~~~

Remove local system infrastructure.

This operation fails if sites are present.  Use the
`--force` option to override.

| Field       | Value |
|------------|-------|
| Platforms  | Kubernetes, Docker, Podman, Linux |

.Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-force">--force</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">



</div>
</div>

.Global options

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
