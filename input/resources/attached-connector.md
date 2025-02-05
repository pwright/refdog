---
refdog_links:
- title: Attached connectors
  url: /topics/attached-connectors.html
- title: AttachedConnectorBinding resource
  url: /resources/attached-connector-binding.html
refdog_object_has_attributes: true
---

# AttachedConnector resource

A connector in a peer namespace.

.Metadata properties

.name
*Type:* `string`

The name of the resource.


The name must be the same as that of the associated
AttachedConnectorBinding resource in the site namespace.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

.namespace
*Type:* `string`

The namespace of the resource.

See also: [Platform concept]({{site_prefix}}/concepts/platform.html), [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

.Spec properties

.siteNamespace
*Type:* `string`

The name of the namespace in which the site this connector
should be attached to is defined.



.port
*Type:* `integer`

The port on the target server to connect to.

Updatable:: True

.selector
*Type:* `string`

A Kubernetes label selector for specifying target server pods.  It
uses `<label-name>=<label-value>` syntax.

On Kubernetes, either `selector` or `host` is required.

Updatable:: True
See also: [Kubernetes label selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors)

.includeNotReadyPods
*Type:* `boolean`

If true, include server pods in the `NotReady` state.

Default:: False

.tlsCredentials
*Type:* `string`

The name of a bundle of TLS certificates used for secure
router-to-server communication.  The bundle contains the trusted
server certificate (usually a CA).  It optionally includes a
client certificate and key for mutual TLS.

On Kubernetes, the value is the name of a Secret in the current
namespace. On Docker, Podman, and Linux, the value is the name of
a directory under `input/certs/` in the current namespace.

See also: [Application TLS]({{site_prefix}}/topics/application-tls.html), [Kubernetes TLS secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets), [System TLS credentials]({{site_prefix}}/topics/system-tls-credentials.html)

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

.conditions
*Type:* `array`

A set of named conditions describing the current state of the
resource.

See also: [Resource status]({{site_prefix}}/topics/resource-status.html), [Kubernetes conditions](https://maelvls.dev/kubernetes-conditions/)

.selectedPods
*Type:* `array`

