---
refdog_links:
  - title: Command overview
    url: overview.md
  - title: Concept index
    url: /concepts/index.md
  - title: Resource index
    url: /resources/index.md
---

## Site operations

### [Site]({{site_prefix}}/commands/site/index.html)

Display help for site commands and exit

#### Subcommands

- [Site create]({{site_prefix}}/commands/site/create.html): Create a site
- [Site update]({{site_prefix}}/commands/site/update.html): Change site settings
- [Site delete]({{site_prefix}}/commands/site/delete.html): Delete a site
- [Site status]({{site_prefix}}/commands/site/status.html): Display the status of a site
- [Site generate]({{site_prefix}}/commands/site/generate.html): Generate a Site resource

## Site linking

### [Token]({{site_prefix}}/commands/token/index.html)

Display help for token commands and exit

#### Subcommands

- [Token issue]({{site_prefix}}/commands/token/issue.html): Issue a token file redeemable for a link to the current site
- [Token redeem]({{site_prefix}}/commands/token/redeem.html): Redeem a token file in order to create a link to a remote site

### [Link]({{site_prefix}}/commands/link/index.html)

Display help for link commands and exit

#### Subcommands

- [Link update]({{site_prefix}}/commands/link/update.html): Change link settings
- [Link delete]({{site_prefix}}/commands/link/delete.html): Delete a link
- [Link status]({{site_prefix}}/commands/link/status.html): Display the status of links in the current site
- [Link generate]({{site_prefix}}/commands/link/generate.html): Generate a Link resource for use in a remote site

## Service exposure

### [Listener]({{site_prefix}}/commands/listener/index.html)

Display help for listener commands and exit

#### Subcommands

- [Listener create]({{site_prefix}}/commands/listener/create.html): Create a listener
- [Listener update]({{site_prefix}}/commands/listener/update.html): Update a listener
- [Listener delete]({{site_prefix}}/commands/listener/delete.html): Delete a listener
- [Listener status]({{site_prefix}}/commands/listener/status.html): Display the status of listeners in the current site
- [Listener generate]({{site_prefix}}/commands/listener/generate.html): Generate a Listener resource

### [Connector]({{site_prefix}}/commands/connector/index.html)

Display help for connector commands and exit

#### Subcommands

- [Connector create]({{site_prefix}}/commands/connector/create.html): Create a connector
- [Connector update]({{site_prefix}}/commands/connector/update.html): Update a connector
- [Connector delete]({{site_prefix}}/commands/connector/delete.html): Delete a connector
- [Connector status]({{site_prefix}}/commands/connector/status.html): Display the status of connectors in the current site
- [Connector generate]({{site_prefix}}/commands/connector/generate.html): Generate a Connector resource

## System operations

### [System]({{site_prefix}}/commands/system/index.html)



#### Subcommands

- [System install]({{site_prefix}}/commands/system/install.html): Install local system infrastructure and configure the environment
- [System uninstall]({{site_prefix}}/commands/system/uninstall.html): Remove local system infrastructure
- [System start]({{site_prefix}}/commands/system/start.html): Start the Skupper router for the current site
- [System stop]({{site_prefix}}/commands/system/stop.html): Stop the Skupper router for the current site
- [System reload]({{site_prefix}}/commands/system/reload.html): Reload the site configuration
- [System apply]({{site_prefix}}/commands/system/apply.html): Create or update resources using files or standard input
- [System delete]({{site_prefix}}/commands/system/delete.html): Delete resources using files or standard input
- [System generate-bundle]({{site_prefix}}/commands/system/generate-bundle.html): Generate a self-contained site bundle for use on another machine

## Debugging operations

### [Debug]({{site_prefix}}/commands/debug/index.html)

Display help for debug commands and exit

#### Subcommands

- [Debug check]({{site_prefix}}/commands/debug/check.html): Run diagnostic checks
- [Debug dump]({{site_prefix}}/commands/debug/dump.html): Generate a debug dump file

## Other operations

### [Version]({{site_prefix}}/commands/version.html)

Display versions of Skupper components
