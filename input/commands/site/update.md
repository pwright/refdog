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

# Site update command

```shell
skupper site update [name] [options]
```

Change site settings.

Platforms:: Kubernetes, Docker, Podman, Linux

Waits for:: Ready


.Examples

```console
# Update the current site to accept links
$ skupper site update --enable-link-access
Waiting for status...
Site "west" is ready.

# Update multiple settings
$ skupper site update --enable-link-access --service-account alice
```

.Primary options

---
**[name]**

Type:: string

Flags:: optional


The name of the site resource.

If not specified, the name is that of the site
associated with the current namespace.

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

---
**--wait**

Type:: <status>


Wait for the given status before exiting.

Default:: ready

Choices:: none:: <em>Do not wait</em>

configured:: Configured

ready:: Ready

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

- **No site resource exists**

  There is no existing Skupper site resource to update.
