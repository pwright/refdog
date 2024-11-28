# Skupper concept overview

<figure>
  <img src="images/overview-1.svg"/>
  <figcaption>The primary concepts in the Skupper model</figcaption>
</figure>

## Sites and networks

Skupper's job is to provide connectivity for applications that have
parts running in multiple locations and on different platforms.

A _site_ represents a particular location and a particular platform.
It's a place where you have real running workloads.

In a distributed application, those workloads need to communicate with
other workloads in other sites.  Skupper uses _links_ between sites to
provide site-to-site communication.

When a set of sites are linked, they function as one
application-focused _network_.

<figure>
  <img src="images/overview-2.svg"/>
  <figcaption>A simple network with two sites</figcaption>
</figure>

Learn more about **[sites](site.html)**,
**[platforms](platform.html)**, **[links](link.html)**, and
**[networks](network.html)**.

## Service exposure

Sites and links establish the network transport, but there is one more step...

<figure>
  <img src="images/overview-3.svg"/>
  <figcaption>A workload exposed as a service in a remote site</figcaption>
</figure>

Learn more about **[listeners](listener.html)**,
**[connectors](connector.html)**, and **[routing
keys](routing-key.html)**.