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
refdog_object_has_attributes: true
---

# Token command

```shell
skupper token [subcommand] [options]
```

Platforms: Kubernetes, Docker, Podman, Linux

## Subcommands

- [Token issue]({{site_prefix}}/commands/token/issue.html): Issue a token file redeemable for a link to the current site
- [Token redeem]({{site_prefix}}/commands/token/redeem.html): Redeem a token file in order to create a link to a remote site
