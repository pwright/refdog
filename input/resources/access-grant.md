---
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Access token concept
  url: /concepts/access-token.html
- title: AccessToken resource
  url: /resources/access-token.html
- title: Token issue command
  url: /commands/token/issue.html
refdog_object_has_attributes: true
---

# AccessGrant resource

Permission to redeem access tokens for links to the local
site.  A remote site can use a token containing the grant
URL and secret code to obtain a certificate signed by the
grant's certificate authority (CA), within a certain
expiration window and for a limited number of redemptions.

The `code`, `url`, and `ca` properties of the resource
status are used to generate access tokens from the grant.

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

.redemptionsAllowed
*Type:* `integer`

The number of times an access token for this grant can
be redeemed.

Default:: 1

.expirationWindow
*Type:* `string (duration)`

The period of time in which an access token for this
grant can be redeemed.

Default:: 15m


.code
*Type:* `string`

The secret code to use to authenticate access tokens submitted
for redemption.

If not set, a value is generated and placed in the `code`
status property.



.issuer
*Type:* `string`

The name of a Kubernetes secret used to generate a
certificate when redeeming a token for this grant.

If not set, `defaultIssuer` on the Site rsource is used.

See also: [Router TLS]({{site_prefix}}/topics/router-tls.html), [Kubernetes TLS secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets)

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

.redemptions
*Type:* `integer`

The number of times a token for this grant has been
redeemed.



.expirationTime
*Type:* `string (date-time)`

The point in time when the grant expires.



.url
*Type:* `string`

The URL of the token-redemption service for this grant.



.ca
*Type:* `string`

The trusted server certificate of the token-redemption
service for this grant.



.code
*Type:* `string`

The secret code used to authenticate access tokens
submitted for redemption.

Default:: <em>Generated</em>


.conditions
*Type:* `array`

A set of named conditions describing the current state of the
resource.


- `Processed`: The controller has accepted the grant.
- `Resolved`: The grant service is available to process tokens
  for this grant.
- `Ready`: The grant is ready to use.  All other
  conditions are true.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html), [Kubernetes conditions](https://maelvls.dev/kubernetes-conditions/)
