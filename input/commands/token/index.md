---
body_class: object command
refdog_object_has_attributes: true
refdog_object_links:
- title: Access token concept
  url: /concepts/access-token.html
- title: AccessGrant resource
  url: /resources/access-grant.html
- title: AccessToken resource
  url: /resources/access-token.html
refdog_object_toc:
- id: ''
  title: Overview
- id: usage
  title: Usage
- id: subcommands
  title: Subcommands
- id: primary-options
  title: Primary options
- id: global-options
  title: Global options
---

# Token command

<section>

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</section>

<section>

## Usage

~~~ shell
skupper token [subcommand] [options]
~~~

</section>

<section>

## Subcommands

<table class="objects">
<tr><th><a href="issue.html">Token issue</a></th><td><p>Issue a token file redeemable for a link to the current site</p>
</td></tr>
<tr><th><a href="redeem.html">Token redeem</a></th><td><p>Redeem a token file in order to create a link to a remote site</p>
</td></tr>
</table>

</section>
