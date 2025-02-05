---
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
refdog_object_has_attributes: true
---

# System generate-bundle command

```shell
skupper system generate-bundle <bundle-file> [options]
```

Generate a self-contained site bundle for use on another
machine.

Platforms:: Kubernetes, Docker, Podman, Linux


.Primary options

---
**&lt;bundle-file&gt;**

Type:: string

Flags:: required


The name of the bundle file to generate.

The command exits with an error if the file already exists.



---
**--input**

Type:: <string>


The location of the Skupper resources defining the site.

Default:: $HOME/.local/share/skupper/namespaces/<namespace>/input/resources


---
**--type**

Type:: <string>


Default:: tarball

Choices:: tarball:: A gzipped tar file

shell-script:: A self-extracting shell script


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


