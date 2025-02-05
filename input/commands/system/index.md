---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
refdog_object_has_attributes: true
---

# System command

```shell
skupper system [subcommand] [options]
```

Platforms:: Kubernetes, Docker, Podman, Linux


.Subcommands

- [System install]({{site_prefix}}/commands/system/install.html): Install local system infrastructure and configure the environment
- [System uninstall]({{site_prefix}}/commands/system/uninstall.html): Remove local system infrastructure
- [System start]({{site_prefix}}/commands/system/start.html): Start the Skupper router for the current site
- [System stop]({{site_prefix}}/commands/system/stop.html): Stop the Skupper router for the current site
- [System reload]({{site_prefix}}/commands/system/reload.html): Reload the site configuration
- [System apply]({{site_prefix}}/commands/system/apply.html): Create or update resources using files or standard input
- [System delete]({{site_prefix}}/commands/system/delete.html): Delete resources using files or standard input
- [System generate-bundle]({{site_prefix}}/commands/system/generate-bundle.html): Generate a self-contained site bundle for use on another machine
