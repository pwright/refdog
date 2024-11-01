---
body_class: object resource
links:
  - name: Listener concept
    url: /concepts/listener.html
  - name: Listener commands
    url: /commands/listener/index.html
  - name: Connector resource
    url: /resources/connector.html
---

# Listener resource

<section>

Binds a connection endpoint in the local site to target
workloads in remote sites.

Each site can have multiple listener definitions.

~~~ yaml
apiVersion: skupper.io/v2alpha1
kind: Listener
~~~

</section>

<section>

## Examples

A listener in site West for the Hello World backend service
in site East:

~~~ yaml
apiVersion: skupper.io/v2alpha1
kind: Listener
metadata:
  name: backend
  namespace: hello-world-west
spec:
  routingKey: backend
  port: 8080
  host: backend
~~~

</section>

<section>

## Metadata properties

- <div class="attribute"><h3 id="metadata-name">name</h3><div>string, required</div></div>

  The name of the resource.

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/names/">Kubernetes object names</a></td></table>

- <div class="attribute"><h3 id="metadata-namespace">namespace</h3><div>string</div></div>

  The namespace of the resource.

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td><tr><th>See also</th><td><a href="/concepts/namespace.html">Namespace concept</a>, <a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/">Kubernetes namespaces</a></td></table>

</section>

<section>

## Spec properties

- <div class="attribute"><h3 id="spec-routingkey">routingKey</h3><div>string, required</div></div>

  The identifier used to route traffic from listeners to
  connectors.  To enable connecting to a service at a
  remote site, the local listener and the remote connector
  must have matching routing keys.

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td><tr><th>See also</th><td><a href="/concepts/routing-key.html">Routing key concept</a></td></table>

- <div class="attribute"><h3 id="spec-host">host</h3><div>string, required</div></div>

  The hostname or IP address of the local listener.  Clients
  at this site use the listener host and port to
  establish connections to the remote service.

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td></table>

- <div class="attribute"><h3 id="spec-port">port</h3><div>integer, required</div></div>

  The port of the local listener.  Clients at this site use
  the listener host and port to establish connections to
  the remote service.

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td></table>

- <div class="attribute"><h3 id="spec-tlscredentials">tlsCredentials</h3><div>string</div></div>

  The name of a Kubernetes secret containing TLS
  credentials.  The secret contains the trusted server
  certificate (typically a CA).
  
  It can optionally include a client certificate and key for
  mutual TLS.
  
  This option is used when setting up client-to-router TLS
  encryption.

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td><tr><th>See also</th><td><a href="">Site-scoped TLS</a></td></table>

- <div class="attribute"><h3 id="spec-type">type</h3><div>string</div></div>

  The listener type.

  <table class="fields"><tr><th>Default</th><td><p><code>tcp</code></p>
  </td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td></table>

- <div class="attribute"><h3 id="spec-settings">settings</h3><div>object</div></div>

  Additional settings.

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td></table>

</section>

<section>

## Status properties

- <div class="attribute"><h3 id="status-matchingconnectorcount">matchingConnectorCount</h3><div>integer</div></div>

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td></table>

  <section class="notes">

  This one has "count" but other counter fields do not.

  </section>

- <div class="attribute"><h3 id="status-status">status</h3><div>string</div></div>

  The current state of the resource.

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td></table>

- <div class="attribute"><h3 id="status-message">message</h3><div>string</div></div>

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td></table>

- <div class="attribute"><h3 id="status-conditions">conditions</h3><div>array</div></div>

  <table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Systemd</td></table>

</section>
