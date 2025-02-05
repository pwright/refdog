---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: System start command
  url: /commands/system/start.html
refdog_object_has_attributes: true
---

# System stop command

```shell
skupper system stop [options]
```

Stop the Skupper router for the current site.  This stops the
systemd service for the current namespace.

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


