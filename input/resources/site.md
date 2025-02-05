---
refdog_links:
- title: Site configuration
  url: /topics/site-configuration.html
- title: Site concept
  url: /concepts/site.html
- title: Site command
  url: /commands/site/index.html
- title: Link resource
  url: /resources/link.html
refdog_object_has_attributes: true
---

# Site resource

A site is a place on the network where application workloads are
running.  Sites are joined by [links](link.html).

The Site resource is the basis for site configuration.  It is the
parent of all Skupper resources in its namespace.  There can be only
one active Site resource per namespace.

.Examples

A minimal site:

```yaml
apiVersion: skupper.io/v2alpha1
kind: Site
metadata:
  name: east
  namespace: hello-world-east
```

A site configured to accept links:

```yaml
apiVersion: skupper.io/v2alpha1
kind: Site
metadata:
  name: west
  namespace: hello-world-west
spec:
  linkAccess: default
```

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

.linkAccess
*Type:* `string`

Configure external access for links from remote sites.

Sites and links are the basis for creating application
networks.  In a simple two-site network, at least one of
the sites must have link access enabled.

Default:: none

Choices:: none:: No linking to this site is permitted.

default:: Use the default link access for the current platform. On OpenShift, the default is <code>route</code>.  For other Kubernetes flavors, the default is <code>loadbalancer</code>.

route:: Use an OpenShift route.  <em>OpenShift only.</em>

loadbalancer:: Use a Kubernetes load balancer.

Updatable:: True
See also: [Link concept]({{site_prefix}}/concepts/link.html), [Site linking]({{site_prefix}}/topics/site-linking.html)

.ha
*Type:* `boolean`

Configure the site for high availability (HA).  HA sites
have two active routers.

Note that Skupper routers are stateless, and they restart
after failure.  This already provides a high level of
availability.  Enabling HA goes further and reduces the
window of downtime caused by restarts.

Default:: False
Updatable:: True
See also: [High availability]({{site_prefix}}/topics/high-availability.html)

.defaultIssuer
*Type:* `string`

The name of a Kubernetes secret containing the signing CA
used to generate a certificate from a token.  A secret is
generated if none is specified.

This issuer is used by AccessGrant and RouterAccess if a
specific issuer is not set.

Default:: skupper-site-ca

Updatable:: True
See also: [Router TLS]({{site_prefix}}/topics/router-tls.html), [Kubernetes TLS secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets)

.edge
*Type:* `boolean`

Configure the site to operate in edge mode.  Edge sites
cannot accept links from remote sites.

Edge mode can help you scale your network to large numbers
of sites.  However, for networks with 16 or fewer sites,
there is little benefit.

Currently, edge sites cannot also have HA enabled.

<!-- Future: An edge site has the exclusive ability to set a
"VAN ID" that enables multiple VANs to operate on shared
router infrastructure. -->

Default:: False
See also: [Large networks]({{site_prefix}}/topics/large-networks.html)

.serviceAccount
*Type:* `string`

The name of the Kubernetes service account under which to run
the Skupper router.  A service account is generated if none is
specified.

Default:: <em>Generated</em>

See also: [Kubernetes service accounts](https://kubernetes.io/docs/concepts/security/service-accounts/)

.settings
*Type:* `object`

A map containing additional settings.  Each map entry has a
string name and a string value.

**Note:** In general, we recommend not changing settings from
their default values.


- `routerDataConnections`: Set the number of data
  connections the router uses when linking to other
  routers.<br/>
  Default: *Computed based on the number of router worker
  threads.  Minimum 2.*
- `routerLogging`: Set the router logging level.<br/>
  Default: `info`.  Choices: `info`, `warning`, `error`.

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


- `Configured`: The output resources for this resource have
  been created.
- `Running`: There is at least one router pod running.
- `Resolved`: The hostname or IP address for link access is
  available.
- `Ready`: The site is ready for use.  All other conditions
  are true.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html), [Kubernetes conditions](https://maelvls.dev/kubernetes-conditions/)

.defaultIssuer
*Type:* `string`

The name of the Kubernetes secret containing the active
default signing CA.

See also: [Router TLS]({{site_prefix}}/topics/router-tls.html), [Kubernetes TLS secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets)

.endpoints
*Type:* `array`

An array of connection endpoints.  Each item has a name, host,
port, and group.

These include connection endpoints for link access.

See also: [Link concept]({{site_prefix}}/concepts/link.html), [Site linking]({{site_prefix}}/topics/site-linking.html)

.network
*Type:* `array`


.sitesInNetwork
*Type:* `integer`
See also: [Network concept]({{site_prefix}}/concepts/network.html)
