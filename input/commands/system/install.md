---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: System uninstall command
  url: /commands/system/uninstall.html
refdog_object_has_attributes: true
---

# System install command

~~~ shell
skupper system install [options]
~~~

Install local system infrastructure and configure the environment.

It does the following:

- Checks the local environment for required resources and
  configuration.
- In some instances, configures the local environment.  On
  Podman, it starts the Podman API service if it is not already
  available.

**Note:** With a long-lived controller, this operation would
also start the controller as a user-scoped systemd service.

| Field       | Value |
|------------|-------|
| Platforms  | Kubernetes, Docker, Podman, Linux |

.Primary options

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
