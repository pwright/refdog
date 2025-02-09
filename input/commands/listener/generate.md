---
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Listener concept
  url: /concepts/listener.html
- title: Listener resource
  url: /resources/listener.html
- title: Connector generate command
  url: /commands/connector/generate.html
- title: Connector command
  url: /commands/connector/index.html
refdog_object_has_attributes: true
---

# Listener generate command

~~~ shell
skupper listener generate <name> <port> [options]
~~~

Generate a Listener resource.

| Field       | Value |
|------------|-------|
| Platforms  | Kubernetes, Docker, Podman, Linux |

.Examples

~~~ console
# Generate a Listener resource and print it to the console
$ skupper listener generate backend 8080
apiVersion: skupper.io/v2alpha1
kind: Listener
metadata:
  name: backend
spec:
  routingKey: backend
  port: 8080
  host: backend

# Generate a Listener resource and direct the output to a file
$ skupper listener generate backend 8080 > backend.yaml
~~~

.Primary options

&lt;name&gt;
required

The name of the resource to be generated.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

&lt;port&gt;
required

The port of the local listener.  Clients at this site use
the listener host and port to establish connections to
the remote service.

Updatable:: True

--routing-key
frequently used

The identifier used to route traffic from listeners to
connectors.  To enable connecting to a service at a
remote site, the local listener and the remote connector
must have matching routing keys.

Default:: <em>Value of name</em>

Updatable:: True

--host
frequently used

The hostname or IP address of the local listener.  Clients
at this site use the listener host and port to
establish connections to the remote service.

Default:: <em>Value of name</em>

Updatable:: True

--wait

Wait for the given status before exiting.

Default:: configured

Choices:: none:: <em>Do not wait</em>

configured:: Configured

ready:: Ready


--output

Select the output format.

Default:: yaml

Choices:: json:: Produce JSON output

yaml:: Produce YAML output


.Global options

--platform
global

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default:: kubernetes

Choices:: kubernetes:: Kubernetes

docker:: Docker

podman:: Podman

linux:: Linux

See also: [Platform concept]({{site_prefix}}/concepts/platform.html)

--help
global

Display help and exit.


