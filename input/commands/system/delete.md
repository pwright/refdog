---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
refdog_object_has_attributes: true
---

# System delete command

```shell
skupper system delete [options]
```

Delete resources using files or standard input.

<!-- File locations and names -->
<!-- Need to run reload after -->

Platforms:: Kubernetes, Docker, Podman, Linux


.Primary options

---
**--filename**

Type:: (-f) <string>




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


