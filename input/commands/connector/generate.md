---
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Connector concept
  url: /concepts/connector.html
- title: Connector resource
  url: /resources/connector.html
- title: Listener generate command
  url: /commands/listener/generate.html
- title: Listener command
  url: /commands/listener/index.html
refdog_object_has_attributes: true
---

# Connector generate command

```shell
skupper connector generate <name> <port> [options]
```

Generate a Connector resource.

Platforms:: Kubernetes, Docker, Podman, Linux


.Examples

```console
# Generate a Connector resource and print it to the console
$ skupper connector generate backend 8080
apiVersion: skupper.io/v2alpha1
kind: Connector
metadata:
  name: backend
spec:
  routingKey: backend
  port: 8080
  selector: app=backend

# Generate a Connector resource and direct the output to a file
$ skupper connector generate backend 8080 > backend.yaml
```

.Primary options

---
**&lt;name&gt;**

Type:: string

Flags:: required


The name of the resource to be generated.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

---
**&lt;port&gt;**

Type:: integer

Flags:: required


The port on the target server to connect to.

Updatable:: True

---
**--routing-key**

Type:: <string>

Flags:: frequently used


The identifier used to route traffic from listeners to
connectors.  To expose a local workload to a remote site, the
remote listener and the local connector must have matching
routing keys.

Default:: <em>Value of name</em>

Updatable:: True

---
**--workload**

Type:: <resource>

Flags:: frequently used


A Kubernetes resource name that identifies a workload.  It uses
`<resource-type>/<resource-name>` syntax and resolves to an
equivalent pod selector.

This is an alternative to setting the `--selector` or
`--host` options.

Platforms:: Kubernetes
See also: [Kubernetes workloads](https://kubernetes.io/docs/concepts/workloads/)

---
**--selector**

Type:: <string>


A Kubernetes label selector for specifying target server pods.  It
uses `<label-name>=<label-value>` syntax.

This is an alternative to setting the `--workload` or
`--host` options.

Default:: app=[value-of-name]

Platforms:: Kubernetes
Updatable:: True
See also: [Kubernetes label selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors)

---
**--host**

Type:: <string>


The hostname or IP address of the server.  This is an
alternative to `selector` for specifying the target server.

This is an alternative to setting the `--selector` or
`--workload` options.

Default:: <em>Value of name</em>

Updatable:: True

---
**--wait**

Type:: <status>


Wait for the given status before exiting.

Default:: configured

Choices:: none:: <em>Do not wait</em>

configured:: Configured

ready:: Ready


---
**--output**

Type:: (-o) <format>


Select the output format.

Default:: yaml

Choices:: json:: Produce JSON output

yaml:: Produce YAML output


.Global options

---
**--platform**

Type:: <platform>

Flags:: global


Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default:: kubernetes

Choices:: kubernetes:: Kubernetes

docker:: Docker

podman:: Podman

linux:: Linux

See also: [Platform concept]({{site_prefix}}/concepts/platform.html)

---
**--help**

Type:: (-h) boolean

Flags:: global


Display help and exit.


