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

~~~ shell
skupper site generate <name> [options]
~~~

Generate a Site resource.

| Field       | Value |
|------------|-------|
| Platforms  | Kubernetes, Docker, Podman, Linux |

.Examples

~~~ console
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
~~~

.Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-name">&lt;name&gt;</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The name of the resource to be generated.

See also: [Kubernetes object names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-enable-link-access">--enable-link-access</h3>
<div class="attribute-type-info">boolean</div>
<div class="attribute-flags">frequently used</div>
</div>
<div class="attribute-body">

Allow external access for links from remote sites.

Sites and links are the basis for creating application
networks. In a simple two-site network, at least one of the
sites must have link access enabled.

See also: [Link concept]({{site_prefix}}/concepts/link.html), [Site linking]({{site_prefix}}/topics/site-linking.html)

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-output">--output</h3>
<div class="attribute-type-info">(-o) &lt;format&gt;</div>
</div>
<div class="attribute-body">

Select the output format.

Default:: yaml

Choices:: json:: Produce JSON output

yaml:: Produce YAML output


</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-link-access-type">--link-access-type</h3>
<div class="attribute-type-info">&lt;type&gt;</div>
</div>
<div class="attribute-body">

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

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-enable-ha">--enable-ha</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

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

</div>
</div>

.Global options

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-platform">--platform</h3>
<div class="attribute-type-info">&lt;platform&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default:: kubernetes

Choices:: kubernetes:: Kubernetes

docker:: Docker

podman:: Podman

linux:: Linux

See also: [Platform concept]({{site_prefix}}/concepts/platform.html)

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">(-h) boolean</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Display help and exit.



</div>
</div>
