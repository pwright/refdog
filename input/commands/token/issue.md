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
- title: Token redeem command
  url: /commands/token/redeem.html
refdog_object_has_attributes: true
---

# Token issue command

~~~ shell
skupper token issue <file> [options]
~~~

Issue a token file redeemable for a link to the current site.

This command first creates an access grant in order to issue
the token.

Issuing a token requires a site with link access enabled.
The command waits for the site to enter the ready state
before producing the token.

| Field       | Value |
|------------|-------|
| Platforms  | Kubernetes |
| Waits for  | Ready |

.Examples

~~~ console
# Issue an access token
$ skupper token issue ~/token.yaml
Waiting for status...
Access grant "west-6bfn6" is ready.
Token file /home/fritz/token.yaml created.

Transfer this file to a remote site. At the remote site,
create a link to this site using the 'skupper token
redeem' command:

    $ skupper token redeem <file>

The token expires after 1 use or after 15 minutes.

# Issue an access token with non-default limits
$ skupper token issue ~/token.yaml --expiration-window 24h --redemptions-allowed 3

# Issue a token using an existing access grant
$ skupper token issue ~/token.yaml --grant west-1
~~~

.Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-file">&lt;file&gt;</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The name of the token file to create.

Platforms:: Kubernetes, Docker, Podman, Linux

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-timeout">--timeout</h3>
<div class="attribute-type-info">&lt;duration&gt;</div>
</div>
<div class="attribute-body">

Raise an error if the operation does not complete in the given
period of time.

Default:: 60s

Platforms:: Kubernetes, Docker, Podman, Linux

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-expiration-window">--expiration-window</h3>
<div class="attribute-type-info">&lt;duration&gt;</div>
</div>
<div class="attribute-body">

The period of time in which an access token for this
grant can be redeemed.

Default:: 15m

Platforms:: Kubernetes, Docker, Podman, Linux

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-redemptions-allowed">--redemptions-allowed</h3>
<div class="attribute-type-info">&lt;integer&gt;</div>
</div>
<div class="attribute-body">

The number of times an access token for this grant can
be redeemed.

Default:: 1
Platforms:: Kubernetes, Docker, Podman, Linux

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-grant">--grant</h3>
<div class="attribute-type-info">&lt;name&gt;</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

Use the named access grant instead of creating a new
one.

Platforms:: Kubernetes, Docker, Podman, Linux

</div>
</div>

.Global options

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-context">--context</h3>
<div class="attribute-type-info">&lt;name&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the kubeconfig context.

See also: [Kubernetes kubeconfigs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-kubeconfig">--kubeconfig</h3>
<div class="attribute-type-info">&lt;file&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the path to the kubeconfig file.

See also: [Kubernetes kubeconfigs](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-namespace">--namespace</h3>
<div class="attribute-type-info">(-n) &lt;name&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the current namespace.

Platforms:: Kubernetes, Docker, Podman, Linux
See also: [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), [System namespaces]({{site_prefix}}/topics/system-namespaces.html)

</div>
</div>

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

Platforms:: Kubernetes, Docker, Podman, Linux
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

Platforms:: Kubernetes, Docker, Podman, Linux

</div>
</div>

.Errors

- **Link access is not enabled**

  Link access at this site is not currently enabled.  You
can use "skupper site update --enable-link-access" to
enable it.

