# Skupper commands

#### Contents
- [Site configuration](#site-configuration)
  - [skupper site](#skupper-site)
  - [skupper site create](#skupper-site-create)
  - [skupper site update](#skupper-site-update)
  - [skupper site delete](#skupper-site-delete)
  - [skupper site status](#skupper-site-status)
- [Site linking](#site-linking)
  - [skupper token](#skupper-token)
  - [skupper token create](#skupper-token-create)
  - [skupper link](#skupper-link)
  - [skupper link create](#skupper-link-create)
  - [skupper link delete](#skupper-link-delete)
  - [skupper link status](#skupper-link-status)
- [Service exposure](#service-exposure)
  - [skupper connector](#skupper-connector)
  - [skupper connector create](#skupper-connector-create)
  - [skupper connector delete](#skupper-connector-delete)
  - [skupper connector status](#skupper-connector-status)
  - [skupper listener](#skupper-listener)
  - [skupper listener create](#skupper-listener-create)
  - [skupper listener delete](#skupper-listener-delete)
  - [skupper listener status](#skupper-listener-status)
- [Debug operations](#debug-operations)
  - [skupper debug](#skupper-debug)
  - [skupper debug dump](#skupper-debug-dump)
- [Other operations](#other-operations)
  - [skupper version](#skupper-version)

## Site configuration

### skupper site

Display help for site commands.


### skupper site create

Create a site.


#### Examples

~~~
# Create a site
skupper site create west

# Create a site that can accept links from remote sites
skupper site create west --enable-link-access
~~~

#### Usage

~~~
skupper site create NAME [options]
~~~

#### Output

~~~
Waiting for status...
Site "<name>" is ready
~~~
#### Options

- **--help**

  Display help and exit.
  

- **--context**

  Select the kubeconfig context.
  

- **--namespace**

  Select the Kubernetes namespace.
  

- **--platform**

  Select the Skupper platform.
  

- **--enable-link-access** (default False)

  Enable external access for links from remote sites.
  

- **--link-access-type** (default _platform dependent_)

  Select the means of opening external access.
  
  The default is `route` on OpenShift and `loadbalancer`
  otherwise.
  

- **--service-account** (default _generated_)

#### Errors

- **Site resource already exists**

  There is already a site resource defined for the namespace.
  

### skupper site update

Change site settings.


#### Examples

~~~
# Update the site to accept links
skupper site update west --enable-link-access

# Update multiple settings
skupper site update west --enable-link-access --link-access-type loadbalancer
~~~

#### Usage

~~~
skupper site update NAME [options]
~~~

#### Output

~~~
Waiting for update to complete...
Site "<name>" is updated
~~~
#### Options

- **--help**

  Display help and exit.
  

- **--context**

  Select the kubeconfig context.
  

- **--namespace**

  Select the Kubernetes namespace.
  

- **--platform**

  Select the Skupper platform.
  

- **--enable-link-access** (default False)

  Enable external access for links from remote sites.
  

- **--link-access-type** (default _platform dependent_)

  Select the means of opening external access.
  
  The default is `route` on OpenShift and `loadbalancer`
  otherwise.
  

- **--service-account** (default _generated_)

#### Errors

- **No site resource exists**

  There is no existing Skupper site resource to update.
  

### skupper site delete

Delete a site.


#### Usage

~~~
skupper site delete NAME
~~~

#### Output

~~~
Waiting for deletion to complete...
Site "<name>" is deleted
~~~
#### Errors

- **No site resource exists**

  There is no existing Skupper site resource to delete.
  

### skupper site status

Show the current status of a site.


#### Usage

~~~
skupper site status
~~~

#### Output

~~~
NAME   STATUS   SITES-IN-NETWORK   SERVICES-IN-NETWORK
west   Ready    1                  0
~~~
#### Options

- **--help**

  Display help and exit.
  

- **--context**

  Select the kubeconfig context.
  

- **--namespace**

  Select the Kubernetes namespace.
  

- **--platform**

  Select the Skupper platform.
  

#### _Notes_

_What is services-in-network?  Is that the total number of_ 
_unique routing keys defined by connectors?  Or listeners?_ 
_Or listeners plus connectors (not the orphans), grouped by_ 
_routing key?_ 

## Site linking

### skupper token

Display help for token commands.  Currently there is just one.


### skupper token create

Create a token.


#### Usage

~~~
skupper token create FILE [options]
~~~

#### Output

~~~
Token file created at <file>
The token expires after 1 use or after 15 minutes
~~~
#### Options

- **--expiry** (default 15m)

- **--uses** (default 1)

### skupper link

Display help for link commands.


### skupper link create

Create a link.


#### Usage

~~~
skupper link create FILE [options]
~~~

#### Output

~~~
Waiting for status...
Link "<name>" is active
You can now safely delete <file>
~~~
#### Options

- **--cost** (default 1)

### skupper link delete


#### Usage

~~~
skupper link delete NAME
~~~

### skupper link status


#### Output

~~~
NAME   STATUS   COST
west   Active   1

Links from remote sites:

None
~~~
## Service exposure

### skupper connector

Display help for connector commands.


### skupper connector create

Create a connector.


#### Usage

~~~
skupper connector create NAME [options]
~~~

#### Output

~~~
Waiting for status...
Connector "<name>" is ready
~~~
#### Options

- **--routing-key** (default _NAME_)

- **--port**

- **--workload**

- **--selector**

- **--host**

### skupper connector delete

Delete a connector.


#### Usage

~~~
skupper connector delete NAME
~~~

#### Output

~~~
Waiting for deletion to complete...
Connector "<name>" is deleted
~~~
### skupper connector status

Show the status of connectors in the current site.


#### Usage

~~~
skupper connector status
~~~

#### Output

~~~
NAME      ROUTING-KEY   SELECTOR      PORT   MATCHING-LISTENERS
backend   backend       app=backend   8080   1
~~~
### skupper listener

Display help for listener commands.


### skupper listener create

Create a listener.


#### Usage

~~~
skupper listener create NAME [options]
~~~

#### Output

~~~
Waiting for status...
Listener "<name>" is ready
~~~
#### Options

- **--routing-key** (default _NAME_)

- **--host**

- **--port**

### skupper listener delete

Delete a listener.


#### Usage

~~~
skupper listener delete NAME
~~~

#### Output

~~~
Waiting for deletion to complete...
Listener "<name>" is deleted
~~~
### skupper listener status

Show the status of listeners in the current site.


#### Usage

~~~
skupper listener status
~~~

#### Output

~~~
NAME      ROUTING-KEY   HOST      PORT   MATCHING-CONNECTORS
backend   backend       backend   8080   1
~~~
## Debug operations

### skupper debug

Display help for debug commands.


### skupper debug dump

Generate a debug dump file.


#### Usage

~~~
skupper debug dump [FILE]
~~~

#### Output

~~~
Debug dump file generated at <file>
~~~
## Other operations

### skupper version


