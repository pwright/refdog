---
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Link concept
  url: /concepts/link.html
- title: Link resource
  url: /resources/link.html
- title: Token command
  url: /commands/token/index.html
refdog_object_has_attributes: true
---

# Link status command

```shell
skupper link status [name] [options]
```

Display the status of links in the current site.

Platforms: Kubernetes, Docker, Podman, Linux

## Examples

```console
# Show the status of all links in the current site
$ skupper link status
NAME          STATUS   COST
west-6bfn6    Ready    1
south-ac619   Error    10

Links from remote sites:

<none>

# Show the status of one link
$ skupper link status west-6bfn6
Name:     west-6bfn6
Status:   Ready
Message:  <none>
Cost:     1
```

## Primary options

[name]
Type: string
Flags:: optional

An optional resource name.  If set, the status command reports
status for the named resource only.

See also: Kubernetes object names (https://kubernetes.io/docs/concepts/overview/working-with-objects/names/)

--timeout
Type: <duration>

Raise an error if the operation does not complete in the given
period of time.

Default: <p>60s</p>

Platforms: Kubernetes
See also: Duration format (https://pkg.go.dev/time#ParseDuration)

--output
Type: (-o) <format>

Print status to the console in a structured output format.

Choices: json: <p>Produce JSON output</p>

yaml: <p>Produce YAML output</p>


## Global options

--context
Type: <name>
Flags:: global

Set the kubeconfig context.

Platforms: Kubernetes
See also: Kubernetes kubeconfigs (https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

--kubeconfig
Type: <file>
Flags:: global

Set the path to the kubeconfig file.

Platforms: Kubernetes
See also: Kubernetes kubeconfigs (https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

--namespace
Type: (-n) <name>
Flags:: global

Set the current namespace.

See also: Kubernetes namespaces (https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/), System namespaces ({{site_prefix}}/topics/system-namespaces.html)

--platform
Type: <platform>
Flags:: global

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

Default: <p>kubernetes</p>

Choices: kubernetes: <p>Kubernetes</p>

docker: <p>Docker</p>

podman: <p>Podman</p>

linux: <p>Linux</p>

See also: Platform concept ({{site_prefix}}/concepts/platform.html)

--help
Type: (-h) boolean
Flags:: global

Display help and exit.


