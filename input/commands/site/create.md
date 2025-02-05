---
refdog_links:
- title: Site configuration
  url: /topics/site-configuration.html
- title: Site concept
  url: /concepts/site.html
- title: Site resource
  url: /resources/site.html
refdog_object_has_attributes: true
---

# Site create command

```shell
skupper site create <name> [options]
```

Create a site.

Platforms:: Kubernetes, Docker, Podman, Linux

Waits for:: Ready


.Examples

```console
# Create a site
$ skupper site create west
Waiting for status...
Site "west" is ready.

# Create a site that can accept links from remote sites
$ skupper site create west --enable-link-access
```

.Primary options

---
**&lt;name&gt;**

Type:: string

Flags:: required


A name of your choice for the Skupper site.  This name is
displayed in the console and CLI output.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

---
**--enable-link-access**

Type:: boolean

Flags:: frequently used


Allow external access for links from remote sites.

Sites and links are the basis for creating application
networks. In a simple two-site network, at least one of the
sites must have link access enabled.

See also: [Link concept]({{site_prefix}}/concepts/link.html), [Site linking]({{site_prefix}}/topics/site-linking.html)

---
**--link-access-type**

Type:: <type>


Configure external access for links from remote sites.

Sites and links are the basis for creating application
networks.  In a simple two-site network, at least one of
the sites must have link access enabled.

Default:: default

Choices:: default:: Use the default link access.  On OpenShift, the default is <code>route</code>.  For other Kubernetes flavors, the default is <code>loadbalancer</code>.

route:: Use an OpenShift route.  <em>OpenShift only.</em>

loadbalancer:: Use a Kubernetes load balancer.  <em>Kubernetes only.</em>

Platforms:: Kubernetes
Updatable:: True
See also: [Site linking]({{site_prefix}}/topics/site-linking.html)

---
**--enable-ha**

Type:: boolean


Configure the site for high availability (HA).  HA sites
have two active routers.

Note that Skupper routers are stateless, and they restart
after failure.  This already provides a high level of
availability.  Enabling HA goes further and reduces the
window of downtime caused by restarts.

Default:: False
Platforms:: Kubernetes
Updatable:: True
See also: [High availability]({{site_prefix}}/topics/high-availability.html)

---
**--timeout**

Type:: <duration>


Raise an error if the operation does not complete in the given
period of time.

Default:: 60s

Platforms:: Kubernetes
See also: [Duration format](https://pkg.go.dev/time#ParseDuration)

---
**--wait**

Type:: <status>


Wait for the given status before exiting.

Default:: ready

Choices:: none:: Do not wait.

configured:: Wait until the configuration is applied.

ready:: Wait until the resource is ready to use.

Platforms:: Kubernetes
See also: [Resource status]({{site_prefix}}/topics/resource-status.html)

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



.Errors

- **A site resource already exists**

  There is already a site resource defined for the namespace.
