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

# Site generate command

```shell
skupper site generate <name> [options]
```

Generate a Site resource.

Platforms:: Kubernetes, Docker, Podman, Linux


.Examples

```console
# Generate a Site resource and print it to the console
$ skupper site generate west --enable-link-access
apiVersion: skupper.io/v2alpha1
kind: Site
metadata:
  name: west
spec:
  linkAccess: default

# Generate a Site resource and direct the output to a file
$ skupper site generate east > east.yaml
```

.Primary options

---
**&lt;name&gt;**

Type:: string

Flags:: required


The name of the resource to be generated.

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
**--output**

Type:: (-o) <format>


Select the output format.

Default:: yaml

Choices:: json:: Produce JSON output

yaml:: Produce YAML output


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

.Global options

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


