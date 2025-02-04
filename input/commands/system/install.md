---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: System uninstall command
  url: /commands/system/uninstall.html
refdog_object_has_attributes: true
---

# System install command

```shell
skupper system install [options]
```

Install local system infrastructure and configure the environment.

It does the following:

- Checks the local environment for required resources and
  configuration.
- In some instances, configures the local environment.  On
  Podman, it starts the Podman API service if it is not already
  available.

**Note:** With a long-lived controller, this operation would
also start the controller as a user-scoped systemd service.

Platforms: Kubernetes, Docker, Podman, Linux

## Primary options

## Global options

--platform
Type: <platform>
Flags:: global

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default: <p>kubernetes</p>

Choices: kubernetes: <p>Kubernetes</p>

docker: <p>Docker</p>

podman: <p>Podman</p>

linux: <p>Linux</p>

See also: Platform concept ({{site_prefix}}/concepts/platform.html)

--help
Type: (-h) boolean
Flags:: global

Display help and exit.


