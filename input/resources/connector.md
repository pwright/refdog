---
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Connector concept
  url: /concepts/connector.html
- title: Connector command
  url: /commands/connector/index.html
- title: Listener resource
  url: /resources/listener.html
refdog_object_has_attributes: true
---

# Connector resource

A connector binds a local workload to [listeners](listener.html) in
remote [sites](site.html).  Listeners and connectors are matched by
routing key.

On Kubernetes, a Connector resource has a selector and port for
specifying workload pods.

On Docker, Podman, and Linux, a Connector resource has a host and
port for specifying a local server.  Optionally, Kubernetes can also
use a host and port.

## Examples

A connector in site East for the Hello World backend service:

~~~ yaml
apiVersion: skupper.io/v2alpha1
kind: Connector
metadata:
  name: backend
  namespace: hello-world-east
spec:
  routingKey: backend
  selector: app=backend
  port: 8080
~~~

## Metadata properties

<div class="attribute">
<div class="attribute-heading">
<h3 id="metadata-name">name</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The name of the resource.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="metadata-namespace">namespace</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The namespace of the resource.

See also: [Platform concept]({{site_prefix}}/concepts/platform.html), [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

</div>
</div>

## Spec properties

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-routing-key">routingKey</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The identifier used to route traffic from listeners to
connectors.  To expose a local workload to a remote site, the
remote listener and the local connector must have matching
routing keys.

Updatable:: True
See also: [Routing key concept]({{site_prefix}}/concepts/routing-key.html)

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-port">port</h3>
<div class="attribute-type-info">integer</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The port on the target server to connect to.

Updatable:: True

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-selector">selector</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">frequently used</div>
</div>
<div class="attribute-body">

A Kubernetes label selector for specifying target server pods.  It
uses `<label-name>=<label-value>` syntax.

On Kubernetes, either `selector` or `host` is required.

Updatable:: True
See also: [Kubernetes label selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors)

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-host">host</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">frequently used</div>
</div>
<div class="attribute-body">

The hostname or IP address of the server.  This is an
alternative to `selector` for specifying the target server.

On Kubernetes, either `selector` or `host` is required.

On Docker, Podman, or Linux, `host` is required.

Updatable:: True

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-include-not-ready-pods">includeNotReadyPods</h3>
<div class="attribute-type-info">boolean</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

If true, include server pods in the `NotReady` state.

Default:: False

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-expose-pods-by-name">exposePodsByName</h3>
<div class="attribute-type-info">boolean</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

If true, expose each pod as an individual service.

Default:: False
See also: [Individual pod services]({{site_prefix}}/topics/individual-pod-services.html)

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-tls-credentials">tlsCredentials</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

The name of a bundle of TLS certificates used for secure
router-to-server communication.  The bundle contains the trusted
server certificate (usually a CA).  It optionally includes a
client certificate and key for mutual TLS.

On Kubernetes, the value is the name of a Secret in the current
namespace. On Docker, Podman, and Linux, the value is the name of
a directory under `input/certs/` in the current namespace.

See also: [Application TLS]({{site_prefix}}/topics/application-tls.html), [Kubernetes TLS secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets), [System TLS credentials]({{site_prefix}}/topics/system-tls-credentials.html)

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-use-client-cert">useClientCert</h3>
<div class="attribute-type-info">boolean</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

Send the client certificate when connecting in order to enable
mutual TLS.

Default:: False
See also: [Application TLS]({{site_prefix}}/topics/application-tls.html)

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-verify-hostname">verifyHostname</h3>
<div class="attribute-type-info">boolean</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

If true, require that the hostname of the server connected to
matches the hostname in the server's certificate.

Default:: False
See also: [Application TLS]({{site_prefix}}/topics/application-tls.html)

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

**Note:** In general, we recommend not changing settings from
their default values.

See also: [Resource settings]({{site_prefix}}/topics/resource-settings.html)

</div>
</div>

## Status properties

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-status">status</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The current state of the resource.

- `Pending`: The resource is being processed.
- `Error`: There was an error processing the resource.  See
  `message` for more information.
- `Ready`: The resource is ready to use.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html)

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-message">message</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

A human-readable status message.  Error messages are reported
here.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html)

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-has-matching-listener">hasMatchingListener</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

True if there is at least one listener with a matching routing
key (usually in a remote site).

Default:: False
See also: [Routing key concept]({{site_prefix}}/concepts/routing-key.html)

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

- `Configured`: The connector configuration has been applied
  to the router.
- `Matched`: There is at least one listener corresponding to
  this connector.
- `Ready`: The connector is ready to use.  All other conditions
  are true.



</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="status-selected-pods">selectedPods</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">



</div>
</div>
