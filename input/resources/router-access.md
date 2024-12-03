---
body_class: object resource
refdog_object_has_attributes: true
refdog_object_links:
- title: Site linking
  url: /concepts/overview.html#site-linking
- title: Site resource
  url: /resources/site.html
- title: Link resource
  url: /resources/link.html
refdog_object_toc:
- id: ''
  title: Overview
- id: metadata-properties
  title: Metadata properties
- id: spec-properties
  title: Spec properties
- id: status-properties
  title: Status properties
---

# RouterAccess resource

<section>

Configuration for secure access to the site router.  The
configuration includes TLS credentials and router ports.

~~~ yaml
apiVersion: skupper.io/v2alpha1
kind: RouterAccess
~~~

</section>

<section class="attributes">

## Metadata properties

</section>

<section class="attributes">

## Spec properties

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-roles">roles</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-tlscredentials">tlsCredentials</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The name of a bundle of TLS certificates and keys used for
secure router-to-router communication.  The bundle
contains the trusted server certificate.  It optionally
includes a client certificate and key for mutual TLS.

On Kubernetes, the value is the name of a Secret in the
current namespace.

On Docker, Podman, and Linux, the value is the name of a
directory under `input/certs/` in the current namespace.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/router-tls.html">Router TLS</a>, <a href="https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets">Kubernetes TLS secrets</a>, <a href="{{site_prefix}}/topics/system-tls-credentials.html">System TLS credentials</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-generatetlscredentials">generateTlsCredentials</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

<table class="fields"><tr><th>Default</th><td>False</td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-issuer">issuer</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-accesstype">accessType</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-bindhost">bindHost</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The hostname or IP address of the network interface to bind
to.  By default, Skupper binds all the interfaces on the host.

<table class="fields"><tr><th>Default</th><td><p><code>0.0.0.0</code></p>
</td><tr><th>Platforms</th><td>Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-subjectalternativenames">subjectAlternativeNames</h3>
<div class="attribute-type-info">array</div>
</div>
<div class="attribute-body">

The hostnames and IPs secured by the router TLS certificate.

<table class="fields"><tr><th>Default</th><td><p><em>The current hostname and the IP address of each bound network
interface</em></p>
</td><tr><th>Platforms</th><td>Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-settings">settings</h3>
<div class="attribute-type-info">object</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

A map containing additional settings.  Each map entry has a
string name and a string value.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/resource-settings.html">Resource settings</a></td></table>

</div>
</div>

</section>

<section class="attributes">

## Status properties

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="status-status">status</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The current state of the resource.

- Pending
- Ready

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/resource-status.html">Resource status</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="status-message">message</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

A human-readable status message.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/resource-status.html">Resource status</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="status-endpoints">endpoints</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

An array of connection endpoints.  Each item has a name, host,
port, and group.

<!-- To what purpose? -->

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="status-conditions">conditions</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

A set of named conditions describing the current state of the
resource.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/resource-status.html">Resource status</a>, <a href="https://maelvls.dev/kubernetes-conditions/">Kubernetes conditions</a></td></table>

</div>
</div>

</section>