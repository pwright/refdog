---
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Access token concept
  url: /concepts/access-token.html
- title: Access token concept
  url: /concepts/access-token.html
- title: AccessGrant resource
  url: /resources/access-grant.html
- title: Token issue command
  url: /commands/token/issue.html
- title: Token redeem command
  url: /commands/token/redeem.html
refdog_object_has_attributes: true
---

# AccessToken resource

A short-lived credential used to create a link.  An access token
contains the URL and secret code of a corresponding access grant.

**Note:** Access tokens are often [issued][issue] and
[redeemed][redeem] using the Skupper CLI.

[issue]: {{site_prefix}}/commands/token/issue.html
[redeem]: {{site_prefix}}/commands/token/redeem.html

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

.url
*Type:* `string`

The URL of the grant service at the remote site.



.code
*Type:* `string`

The secret code used to authenticate the token when
submitted for redemption.



.ca
*Type:* `string`

The trusted server certificate of the grant service at the
remote site.



.linkCost
*Type:* `integer`

The link cost to use when creating the link.

Default:: 1
See also: [Load balancing]({{site_prefix}}/topics/load-balancing.html)

.settings
*Type:* `object`

A map containing additional settings.  Each map entry has a
string name and a string value.

**Note:** In general, we recommend not changing settings from
their default values.

See also: [Resource settings]({{site_prefix}}/topics/resource-settings.html)

.Status properties

.redeemed
*Type:* `boolean`

True if the token has been redeemed.  Once a token is
redeemed, it cannot be used again.

Default:: False

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


- `Redeemed`: The token has been exchanged for a link.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html), [Kubernetes conditions](https://maelvls.dev/kubernetes-conditions/)
