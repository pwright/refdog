---
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Site resource
  url: /resources/site.html
- title: Link resource
  url: /resources/link.html
refdog_object_has_attributes: true
---

# RouterAccess resource

Configuration for secure access to the site router.  The
configuration includes TLS credentials and router ports.  The
RouterAccess resource is used to implement link access for sites.

.Metadata properties

.name
*Type:* `string`

The name of the resource.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

.namespace
*Type:* `string`

The namespace of the resource.

See also: [Platform concept]({{site_prefix}}/concepts/platform.html), [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

.Spec properties

.roles
*Type:* `array`

The named interfaces by which a router can be accessed.  These
include "inter-router" for links between interior routers and
"edge" for links from edge routers to interior routers.



.tlsCredentials
*Type:* `string`

The name of a bundle of TLS certificates used for mutual TLS
router-to-router communication.  The bundle contains the
server certificate and key and the trusted client certificate
(usually a CA).

On Kubernetes, the value is the name of a Secret in the
current namespace.

On Docker, Podman, and Linux, the value is the name of a
directory under `input/certs/` in the current namespace.

See also: [Router TLS]({{site_prefix}}/topics/router-tls.html), [Kubernetes TLS secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets), [System TLS credentials]({{site_prefix}}/topics/system-tls-credentials.html)

.generateTlsCredentials
*Type:* `boolean`
Default:: False

.issuer
*Type:* `string`


.accessType
*Type:* `string`
Default:: <em>On OpenShift, the default is <code>route</code>.  For other
Kubernetes flavors, the default is <code>loadbalancer</code>.</em>

Choices:: route:: Use an OpenShift route.  <em>OpenShift only.</em>

loadbalancer:: Use a Kubernetes load balancer.


.bindHost
*Type:* `string`

The hostname or IP address of the network interface to bind
to.  By default, Skupper binds all the interfaces on the host.

Default:: 0.0.0.0


.subjectAlternativeNames
*Type:* `array`

The hostnames and IPs secured by the router TLS certificate.

Default:: <em>The current hostname and the IP address of each bound network
interface</em>


.settings
*Type:* `object`

A map containing additional settings.  Each map entry has a
string name and a string value.

**Note:** In general, we recommend not changing settings from
their default values.

See also: [Resource settings]({{site_prefix}}/topics/resource-settings.html)

.Status properties

.status
*Type:* `string`

The current state of the resource.

- `Pending`: The resource is being processed.
- `Error`: There was an error processing the resource.  See
  `message` for more information.
- `Ready`: The resource is ready to use.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html)

.message
*Type:* `string`

A human-readable status message.  Error messages are reported
here.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html)

.conditions
*Type:* `array`

A set of named conditions describing the current state of the
resource.


- `Configured`: The router access configuration has been applied to
  the router.
- `Resolved`: The connection endpoints are available.
- `Ready`: The router access is ready to use.  All other
  conditions are true.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html), [Kubernetes conditions](https://maelvls.dev/kubernetes-conditions/)

.endpoints
*Type:* `array`

An array of connection endpoints.  Each item has a name, host,
port, and group.


