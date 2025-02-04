---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
refdog_object_has_attributes: true
---

# System reload command

```shell
skupper system reload [options]
```

Reload the site configuration.  This restarts the systemd
service for the current namespace.

**Note:** This is currently equivalent to start then stop.  With
a router adaptor service, we could avoid a router restart for some
config changes.

Platforms: Kubernetes, Docker, Podman, Linux
