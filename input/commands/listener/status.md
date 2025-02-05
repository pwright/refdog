---
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Listener concept
  url: /concepts/listener.html
- title: Listener resource
  url: /resources/listener.html
- title: Connector status command
  url: /commands/connector/status.html
- title: Connector command
  url: /commands/connector/index.html
refdog_object_has_attributes: true
---

# Listener status command

```shell
skupper listener status [name] [options]
```

Display the status of listeners in the current site.

Platforms:: Kubernetes, Docker, Podman, Linux


.Examples

```console
# Show the status of all listeners in the current site
$ skupper listener status
NAME       STATUS   ROUTING-KEY   HOST       PORT   CONNECTORS
backend    Ready    backend       backend    8080   true
database   Ready    database      database   5432   true

# Show the status of one listener
$ skupper listener status backend
Name:                      backend
Status:                    Ready
Message:                   <none>
Routing key:               backend
Host:                      backend
Port:                      8080
Has matching connectors:   true
```

.Primary options

---
**[name]**

Type:: string

Flags:: optional


An optional resource name.  If set, the status command reports
status for the named resource only.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

---
**--timeout**

Type:: <duration>


Raise an error if the operation does not complete in the given
period of time.

Default:: 60s

Platforms:: Kubernetes
See also: [Duration format](https://pkg.go.dev/time#ParseDuration)

---
**--output**

Type:: (-o) <format>


Print status to the console in a structured output format.

Choices:: json:: Produce JSON output

yaml:: Produce YAML output


.Global options

---
**--context**

Type:: <name>

Flags:: global


Set the kubeconfig context.

Platforms:: Kubernetes
See also: [Kubernetes kubeconfigs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

---
**--kubeconfig**

Type:: <file>

Flags:: global


Set the path to the kubeconfig file.

Platforms:: Kubernetes
See also: [Kubernetes kubeconfigs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

---
**--namespace**

Type:: (-n) <name>

Flags:: global


Set the current namespace.

See also: [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

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


