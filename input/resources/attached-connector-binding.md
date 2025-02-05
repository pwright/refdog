---
refdog_links:
- title: Attached connectors
  url: /topics/attached-connectors.html
- title: AttachedConnector resource
  url: /resources/attached-connector.html
refdog_object_has_attributes: true
---

# AttachedConnectorBinding resource

A binding to an attached connector in a peer namespace.

.Metadata properties

.name
*Type:* `string`

The name of the resource.


The name must be the same as that of the associated
AttachedConnector resource in the connector namespace.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

.namespace
*Type:* `string`

The namespace of the resource.

See also: [Platform concept]({{site_prefix}}/concepts/platform.html), [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

.Spec properties

.connectorNamespace
*Type:* `string`

The name of the namespace where the associated
AttachedConnector is located.



.routingKey
*Type:* `string`

The identifier used to route traffic from listeners to
connectors.  To expose a local workload to a remote site, the
remote listener and the local connector must have matching
routing keys.

Updatable:: True
See also: [Routing key concept]({{site_prefix}}/concepts/routing-key.html)

.exposePodsByName
*Type:* `boolean`

If true, expose each pod as an individual service.

Default:: False
See also: [Individual pod services]({{site_prefix}}/topics/individual-pod-services.html)

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

.hasMatchingListener
*Type:* `boolean`

True if there is at least one listener with a matching routing
key (usually in a remote site).

Default:: False
See also: [Routing key concept]({{site_prefix}}/concepts/routing-key.html)

.conditions
*Type:* `array`

A set of named conditions describing the current state of the
resource.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html), [Kubernetes conditions](https://maelvls.dev/kubernetes-conditions/)
