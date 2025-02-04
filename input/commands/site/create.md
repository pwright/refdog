---
body_class: object command
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

Platforms: Kubernetes, Docker, Podman, Linux
Waits for: Ready

## Examples

```console
# Create a site
$ skupper site create west
Waiting for status...
Site "west" is ready.

# Create a site that can accept links from remote sites
$ skupper site create west --enable-link-access
```

## Primary options

&lt;name&gt;
Type: string
Flags: required

A name of your choice for the Skupper site.  This name is
displayed in the console and CLI output.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/names/">Kubernetes object names</a></td></table>

--enable-link-access
Type: boolean
Flags: frequently used

Allow external access for links from remote sites.

Sites and links are the basis for creating application
networks. In a simple two-site network, at least one of the
sites must have link access enabled.

<table class="fields"><tr><th>See also</th><td><a href="{{site_prefix}}/concepts/link.html">Link concept</a>, <a href="{{site_prefix}}/topics/site-linking.html">Site linking</a></td></table>

--link-access-type
Type: <type>

Configure external access for links from remote sites.

Sites and links are the basis for creating application
networks.  In a simple two-site network, at least one of
the sites must have link access enabled.

<table class="fields"><tr><th>Default</th><td><p><code>default</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>default</code></th><td><p>Use the default link access.  On OpenShift, the default is <code>route</code>.  For other Kubernetes flavors, the default is <code>loadbalancer</code>.</p>
</td></tr><tr><th><code>route</code></th><td><p>Use an OpenShift route.  <em>OpenShift only.</em></p>
</td></tr><tr><th><code>loadbalancer</code></th><td><p>Use a Kubernetes load balancer.  <em>Kubernetes only.</em></p>
</td></tr></table></td><tr><th>Platforms</th><td>Kubernetes</td><tr><th>Updatable</th><td>True</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/site-linking.html">Site linking</a></td></table>

--enable-ha
Type: boolean

Configure the site for high availability (HA).  HA sites
have two active routers.

Note that Skupper routers are stateless, and they restart
after failure.  This already provides a high level of
availability.  Enabling HA goes further and reduces the
window of downtime caused by restarts.

<table class="fields"><tr><th>Default</th><td>False</td><tr><th>Platforms</th><td>Kubernetes</td><tr><th>Updatable</th><td>True</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/high-availability.html">High availability</a></td></table>

--timeout
Type: <duration>

Raise an error if the operation does not complete in the given
period of time.

<table class="fields"><tr><th>Default</th><td><p><code>60s</code></p>
</td><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="https://pkg.go.dev/time#ParseDuration">Duration format</a></td></table>

--wait
Type: <status>

Wait for the given status before exiting.

<table class="fields"><tr><th>Default</th><td><p><code>ready</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>none</code></th><td><p>Do not wait.</p>
</td></tr><tr><th><code>configured</code></th><td><p>Wait until the configuration is applied.</p>
</td></tr><tr><th><code>ready</code></th><td><p>Wait until the resource is ready to use.</p>
</td></tr></table></td><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="{{site_prefix}}/topics/resource-status.html">Resource status</a></td></table>

## Global options

--context
Type: <name>
Flags: global

Set the kubeconfig context.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Kubernetes kubeconfigs</a></td></table>

--kubeconfig
Type: <file>
Flags: global

Set the path to the kubeconfig file.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Kubernetes kubeconfigs</a></td></table>

--namespace
Type: (-n) <name>
Flags: global

Set the current namespace.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/">Kubernetes namespaces</a>, <a href="{{site_prefix}}/topics/system-namespaces.html">System namespaces</a></td></table>

--platform
Type: <platform>
Flags: global

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

<table class="fields"><tr><th>Default</th><td><p><code>kubernetes</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>kubernetes</code></th><td><p>Kubernetes</p>
</td></tr><tr><th><code>docker</code></th><td><p>Docker</p>
</td></tr><tr><th><code>podman</code></th><td><p>Podman</p>
</td></tr><tr><th><code>linux</code></th><td><p>Linux</p>
</td></tr></table></td><tr><th>See also</th><td><a href="{{site_prefix}}/concepts/platform.html">Platform concept</a></td></table>

--help
Type: (-h) boolean
Flags: global

Display help and exit.



## Errors

- **A site resource already exists**

  <p>There is already a site resource defined for the namespace.</p>
