---
body_class: object command
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

```shell
skupper token issue <file> [options]
```

Issue a token file redeemable for a link to the current site.

This command first creates an access grant in order to issue
the token.

Issuing a token requires a site with link access enabled.
The command waits for the site to enter the ready state
before producing the token.

Platforms: Kubernetes
Waits for: Ready

## Examples

```console
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
```

## Primary options

&lt;file&gt;
Type: string
Flags: required

The name of the token file to create.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

--timeout
Type: <duration>

Raise an error if the operation does not complete in the given
period of time.

<table class="fields"><tr><th>Default</th><td><p><code>60s</code></p>
</td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

--expiration-window
Type: <duration>

The period of time in which an access token for this
grant can be redeemed.

<table class="fields"><tr><th>Default</th><td><p><code>15m</code></p>
</td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

--redemptions-allowed
Type: <integer>

The number of times an access token for this grant can
be redeemed.

<table class="fields"><tr><th>Default</th><td>1</td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

--grant
Type: <name>
Flags: advanced

Use the named access grant instead of creating a new
one.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Global options

--context
Type: <name>
Flags: global

Set the kubeconfig context.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Kubernetes kubeconfigs</a></td></table>

--kubeconfig
Type: <file>
Flags: global

Set the path to the kubeconfig file.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Kubernetes kubeconfigs</a></td></table>

--namespace
Type: (-n) <name>
Flags: global

Set the current namespace.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/">Kubernetes namespaces</a>, <a href="{{site_prefix}}/topics/system-namespaces.html">System namespaces</a></td></table>

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
</td></tr></table></td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>See also</th><td><a href="{{site_prefix}}/concepts/platform.html">Platform concept</a></td></table>

--help
Type: (-h) boolean
Flags: global

Display help and exit.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Errors

- **Link access is not enabled**

  <p>Link access at this site is not currently enabled.  You
can use "skupper site update --enable-link-access" to
enable it.</p>
