---
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Access token concept
  url: /concepts/access-token.html
- title: AccessGrant resource
  url: /resources/access-grant.html
- title: AccessToken resource
  url: /resources/access-token.html
- title: Token issue command
  url: /commands/token/issue.html
refdog_object_has_attributes: true
---

# Token redeem command

```shell
skupper token redeem <file> [options]
```

Redeem a token file in order to create a link to a remote
site.

Platforms:: Kubernetes, Docker, Podman, Linux


.Examples

```console
# Redeem an access token
$ skupper token redeem ~/token.yaml
Waiting for status...
Link "west-6bfn6" is active.
You can now safely delete /home/fritz/token.yaml.
```

.Primary options

---
**&lt;file&gt;**

Type:: string

Flags:: required


The name of the token file to use.



---
**--timeout**

Type:: <duration>


Raise an error if the operation does not complete in the given
period of time.

Default:: 60s


---
**--link-cost**

Type:: <integer>


The link cost to use when creating the link.

Default:: 1
See also: [Load balancing]({{site_prefix}}/topics/load-balancing.html)

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


