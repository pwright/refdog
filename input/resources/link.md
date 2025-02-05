---
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Link concept
  url: /concepts/link.html
- title: Link command
  url: /commands/link/index.html
- title: AccessToken resource
  url: /resources/access-token.html
refdog_object_has_attributes: true
---

# Link resource

A link is a channel for communication between [sites](site.html).
Links carry application connections and requests.  A set of linked
sites constitutes a network.

A Link resource specifies remote connection endpoints and TLS
credentials for establishing a mutual TLS connection to a remote
site.  To create an active link, the remote site must first enable
_link access_.  Link access provides an external access point for
accepting links.

**Note:** Links are not usually created directly.  Instead, you can
use an [access token][token] to obtain a link.

[token]: access-token.html

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

.endpoints
*Type:* `array`

An array of connection endpoints. Each item has a name, host,
port, and group.



.cost
*Type:* `integer`

The configured routing cost of sending traffic over
the link.

Default:: 1
See also: [Load balancing]({{site_prefix}}/topics/load-balancing.html)

.tlsCredentials
*Type:* `string`

The name of a bundle of certificates used for mutual TLS
router-to-router communication.  The bundle contains the
client certificate and key and the trusted server certificate
(usually a CA).

On Kubernetes, the value is the name of a Secret in the
current namespace.

On Docker, Podman, and Linux, the value is the name of a
directory under `input/certs/` in the current namespace.

See also: [Router TLS]({{site_prefix}}/topics/router-tls.html), [Kubernetes TLS secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets), [System TLS credentials]({{site_prefix}}/topics/system-tls-credentials.html)

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

.remoteSiteId
*Type:* `string`

The unique ID of the site linked to.



.remoteSiteName
*Type:* `string`

The name of the site linked to.



.conditions
*Type:* `array`

A set of named conditions describing the current state of the
resource.


- `Configured`: The link configuration has been applied to
  the router.
- `Operational`: The link to the remote site is active.
- `Ready`: The link is ready to use.  All other conditions
  are true.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html), [Kubernetes conditions](https://maelvls.dev/kubernetes-conditions/)
