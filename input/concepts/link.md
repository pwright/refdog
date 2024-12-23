---
body_class: object concept
refdog_object_links:
- title: Link resource
  url: /resources/link.html
- title: Link command
  url: /commands/link/index.html
- title: Network concept
  url: /concepts/network.html
- title: Site concept
  url: /concepts/site.html
- title: Access token concept
  url: /concepts/access-token.html
---

# Link concept

<section>

A ***link*** is a channel for communication between sites.  Links
serve as a transport for application connections and requests.  A
set of linked sites constitutes a network.

To create a link to a remote site, the remote site must provide
***link access***.  A link access is an external access point for
accepting links.

Application connections and requests flow across links in both
directions.  A linked site can communicate with any other site
in the network of sites, even if it is not linked directly.

Links are encrypted and authenticated using mutual TLS.  You can
use access tokens to create links.

<figure>
  <img src="images/link-1.svg"/>
  <figcaption>A link joining two sites to create a simple network</figcaption>
</figure>

<figure>
  <img src="images/link-2.svg"/>
  <figcaption>A site with two links, to two remote sites</figcaption>
</figure>

<figure>
  <img src="images/link-3.svg"/>
  <figcaption>A larger network with links to a central hub site</figcaption>
</figure>

</section>
