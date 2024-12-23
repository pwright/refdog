---
body_class: object concept
refdog_object_links:
- title: Site resource
  url: /resources/site.html
- title: Site command
  url: /commands/site/index.html
- title: Network concept
  url: /concepts/network.html
- title: Link concept
  url: /concepts/link.html
- title: Platform concept
  url: /concepts/platform.html
---

# Site concept

<section>

A ***site*** is a place on the network where workloads are running.
Sites are linked to form application networks.

Sites operate on multiple platforms.  One site corresponds to
one namespace in a platform instance.  Sites can be added to a
network and removed from a network dynamically.

Each site has a Skupper router which is responsible for
communicating with the local workloads and forwarding traffic to
routers in remote sites.

<figure>
  <img src="images/site-1.svg"/>
  <figcaption>A site with three workloads</figcaption>
</figure>

<figure>
  <img src="images/site-2.svg"/>
  <figcaption>Two sites linked to form a network</figcaption>
</figure>

<figure>
  <img src="images/site-3.svg"/>
  <figcaption>A network with sites on three different
  platforms</figcaption>
</figure>

</section>
