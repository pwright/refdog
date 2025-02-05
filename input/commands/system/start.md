---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: System stop command
  url: /commands/system/stop.html
refdog_object_has_attributes: true
---

# System start command

```shell
skupper system start [options]
```

Start the Skupper router for the current site.  This starts the
systemd service for the current namespace.

**Note:** In the absence of a long-lived controller, this
operation first reads the input resources and updates the router
configuration.  With a long-lived controller, that config update
would have already taken place.

Platforms:: Kubernetes, Docker, Podman, Linux


.Primary options

.Global options

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


