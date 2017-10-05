# OOB-REST
A flexible framework for accessing system management information from the hardware that produces it, and distributing it through a RESTful interface.

## Key Features
* RESTful service for OOB information in JSON
* Parallelism out-of-the-box
* Globstar-style search paths for multiple system properties concurrently
* Lightweight (deployable on embedded BMC devices)
* Plugin model for easy extension to new devices
* Configurable system architecture, so you can map your URLs to your system architecture one-to-one
* SSL and HTTP Basic Auth support

## Getting Started
In just a few moments, we'll start our very own instance of the OOB-REST server!

### Download & Installation
1. Ensure that both Python 3.4 and the correct version of PIP are both installed. On CentOS 7,
this can be done with: `sudo yum install python34 python34-pip`
2. Clone the repository from [css/actsys](https://sid-gerrit.devtools.intel.com/#/admin/projects/css/actsys)
3. Navigate to the `oobrestserver` directory under `actsys`
4. Run `sudo python3 setup.py install` to install the server.

### Running the Test Suite
Run `make coverage`, `make test`, or `python3 -m py.test` from `oobrestserver` (from the repository root)
to run the tests. Installation of the server package is not required to run the tests, but the requirements listed in `oobrestserver/requirements.txt` are needed. `sudo pip3 -r oobrestserver/requirements.txt` to install all the dependencies. This step is not required when using GNU Make, since the included makefile installs all of the dependencies anyway.

### Starting the Server
Start the OOB-REST server by running `oobrestserver`. A configuration file should be provided on the command line; Otherwise, the server will start, but will not actually serve any URLs. Detailed information about how to create configuration files is provided later in this document.

### Command-line Arguments
Argument | Description
-|-
-h, --help | show this help message and exit
--config-file CONFIG_FILE | JSON configuration file routing plugin methods to URLs.
--host HOST | Hostname in format ip:port for server.
--key KEY | Private key file for server. Required with --cert to enable SSL.
--cert CERT | OpenSSL cert file for server. Required with --key to enable SSL.
--auth-file AUTH_FILE | Auth file name. Provide to enable basic auth. Requires SSL Enabled.

### Securing the Server
To enable SSL, provide the server private key and the certificate file on the command line. Now, the server will only fulfill valid HTTPS requests, and will ignore all others.

To enable HTTP basic authorization, provide an "auth file". Auth files contain the hashed passwords and salt values for each username. Auth files can be created or edited with the provided `auth_edit.py` tool.

#### Auth Edit Tool Command-line Arguments
Argument | Description
-|-
-h, --help |show this help message and exit
--auth-file AUTH_FILE | Auth file to edit or create
--add-user ADD_USER | User name to add
--change-pass CHANGE_PASS| User name whose password to change
--remove-user REMOVE_USER| User name to remove

The tool will query the user for new or old passwords as needed.

## Configuration
The purpose of the server configuration file is to define the hierarchy of URLs served by the system, and to connect the terminal nodes of this hierarchy to plugin-driven resources. This is accomplished by defining a nested key-value map in JSON or YAML.

### Basic Structure
The file, parsed in its entirety, defines a hierarchy node which is automatically mounted by the server at the path `/api`.

#### Node
A node in the resource hierarchy is merely a mapping of keys to child objects, which may be either nodes or resources. The sequence of keys used to map from the top-level object to a resource defines the URL which will be used to identify that resource.

For example, the following configuration will attach the resources provided by the plugin `Foo.Bar` at the URL route `/api/foo/bar` and the plugin `Foo.Baz` at `/api/foo/baz`

```
foo:
  bar:
    _attach_plugins:
      - module: Foo.Bar
  baz:
    _attach_plugins:
      - module: Foo.Baz
```

#### The `_attach_plugins` Directive
In the short example above, we saw the key `_attach_plugins` in the maps under `foo/bar` and  `foo/baz`. This is a special key; instead of telling the server that there are more layers of URL hierarchy, it directs the server to instantiate plugins at this level of the hierarchy. The key `_attach_plugins` should always map to a list of special key-value mappings called plugin definitions.

#### Plugin Definitions
Plugin definitions are key-value maps with the following format:

Key | Value
-|-
`module` | The full name of the Python class of the plugin. This shall be the full path, formatted `module_name.class_name`.
`args` | A list object defining the positional arguments passed to the plugin object's `__init__` method.
`kwargs` | A key-value map object defining the keyword arguments passed to the plugin object's `__init__` method.
`url_mods` | A key-value map object describing the transformations to apply to the default resource map provided by this plugin instance.

For example, this configuration file:

```
foo_string:
  _attach_plugins:
    - module: oob_rest_default_providers.StringDevice
      args: [Foo]
      url_mods:
        string: example/hierarchy/my_deep_string
```

constructs an instance of the built-in string-storage device provided with the server package, with the following properties:
* All resources provided by the plugin will be located at URL routes beginning with `api/foo_string`.
* The only positional argument passed to the `__init__` method when creating the instance is the string `Foo`.
* No keyword arguments are given to the `__init__` method.
* The resource that would be provided at the path `string` from this plugin (which would normally be at `api/foo_string/string`) will now be remapped to the new route `example/hierarchy/my_deep_string`. Therefore, the string-storage resource from this plugin will be found at `api/foo_string/example/hierarchy/my_deep_string`

#### More on URL Transformations
The `url_mods` mapping will take globstar-style search terms, so multiple resources may be moved under a single node. These kinds of transformations will preserve the structure of the moved resources.

### Important Built-in providers
Most of the built-in providers are only useful to the test suite; however, a few plugins are provided with the server package to help bootstrap the use of OOB-REST on a new system.

#### Built-in Redirection Provider
The provider `oob_rest_default_providers.Redirect` takes one argument during initialization - the IP address (with port number) of the remote server to "graft" onto the resource tree at this location. When a URL routes through this node, the parts of the route after this node will be copied into a new URL which the client will be redirected to. For parallel operations, the ambiguous path provided will not resolve into any properties hosted by the remote node. That is, the nodes under redirection will only appear for single, unambiguous requests.
> This provider has not been implemented yet. A warning and error message will be generated if a configuration file references this provider.

#### Built-in Aggregation Provider
The provider `oob_rest_default_providers.Aggregate` takes one argument during initialization - the remote server to "graft" onto the tree at this location. When a URL routes through this node, the parts of the route after this node will be copied into a new URL for a new request aimed at the remote server. The request will be issued from the server to the remote server, and the response will be copied back to the client. In the case of parallel operations, all responses will be aggregated in one reply back to the client.
> This provider has not been implemented yet. A warning and error message will be generated if a configuration file references this provider.

#### Performance Notes - Aggregate vs. Redirect
The redirect provider issues more network traffic and does not support parallel operations - so why would a system architecture elect to include it? One possible reason is server performance. Sometimes, it may be beneficial to provide cross-links between low-power devices. This redirection node allows this with minimal server overhead, while the aggregation provider requires that the server issue requests concurrently, and aggregate results.

## Client API
Clients interact with the OOB-REST server by issuing HTTP requests to URLs that the server provides.

### Valid URL
System properties to be served by OOB-REST are organized in a hierarchical way, as described by the server configuration file. Therefore, a valid URL route for an instance of the OOB-REST service is a path that identifies some property of the system.

#### Ambiguity and Parallelism
There is a key duality between ambiguity and parallelism in the OOB-REST model. When a URL route is requested from OOB-REST which contains bash-style wildcarding, the wildcards will be resolved into a list of all matching URL routes that the system supports, and all of the requested operations will execute concurrently. One aggregated response will be returned to the client.

#### Globstar
To support property matching at arbitrary hierarchy depths, the server understands bash "globstars". That is, two wildcard stars in sequence act as a "globstar," which matches at any hierarchy level. For instance, given the following routes:
* `foo/a`
* `bar/a`
* `foo/bar/a`
* `bar/foo/a`

The following matches are possible:

Search | Matches
-|-
`*/a` | `foo/a`, `bar/a`
`*/*/a` | `foo/bar/a`, `bar/foo/a`
`**/a` | `foo/a`, `bar/a`, `foo/bar/a`, `bar/foo/a`

#### URL Parameters
Requests to the OOB-REST server may include URL parameters that configure some of the per-request behavior of the API.

Parameter | Type | Description | Notes
-|-|-|-
`sample_rate` | float | When provided with `duration`, specifies the rate, in Hertz, at which to sample the property. |
`duration` | float | When provided with `sample_rate`, specifies the time, in seconds, over which to sample to property. |
`timeout` | float | The server shall time out after the provided number of seconds, killing all processes related to the request and returning a failure message to the client. | *This argument is not yet implemented, and will be ignored.*
`callback` | string | When provided, a response is given to the client immediately, and the server shall perform a POST operation to the URL provided by this argument when the request is complete. | *This argument is not yet implemented, and will be ignored.*

Any URL parameters other than the ones listed above are passed to the invoked plugin method's `kwargs` dictionary.

### HTTP methods
The only supported HTTP methods are GET and POST. GET corresponds to the defined "get" behavior of a property, and POST corresponds to the "set" behavior.
> Note: Internally, these map to the methods identified as "#getter" and "#setter" by the plugin configuration dictionary, respectively.

#### GET
The body of any GET request to the OOB-REST server will be ignored. The route and parameters supplied as part of the URL are enough to fully specify a GET request.

#### POST
The body of a POST request should contain only the JSON-serialized object the user wishes to pass as an argument to the setter function of the property identified by the route. The request header must be application/json.

### JSON Response Formats
Every response given by the server is a JSON object whose top-level keys are the full paths to resources identified by the requested URL, after disambiguation. The mapped objects describe the state of their respective resources with the following schema.

Key | Value Type | Value Description
-|-
`units` | string | A string identifying the units of measurement for this property. It is optional.
`exceptions` | list of strings | List of strings taken by casting any exceptions encountered by plugins during this operation.
`start-time` | float | The server's system time when the operation started
`samples` | list of objects | The list of JSON-serialized objects returned by the plugin as a response for this property. There may be more than one returned object when  the `duration` and `sample_rate` parameters are given.

For URLs that identify non-terminal nodes of the resource tree, the `units` property is `PathNode` and each value in the `samples` list is a list of valid next-step URL pieces that, when concatenated with the current URL, lead to deeper nodes in the resource tree. This is done to implement `ls`-like functionality.

### Client API Python Wrapper
Provided with the server is a Python wrapper class to handle URLs and HTTP requests for the client. This class, called NodeController, has the following methods:

#### `__init__(self, host)`
The `host` argument is the IP address or hostname, with the port number, of the server. It is a string containing something like `localhost:5000` or `127.0.0.1:80`.

#### `get_value(self, path)`
This function will issue an HTTP GET request to the URL at `path` on the host, and return a Python dictionary representing the parsed JSON response.

#### `set_value(self, path, value)`
This function will issue an HTTP POST request and return a Python dictionary representing the parsed JSON response. The `value` argument specifies the value passed to the HTTP POST request.

#### `get_value_over_time(self, path, duration, sample_rate)`
This function will issue an HTTP GET request for multiple samples of a property over time, and return a Python dictionary representing the parsed JSON response. The `duration` argument specifies the time in seconds to collect data, and the `sample_rate` argument specifies the number of samples to take per second.

## Writing Plugins
A central tenant of the design of OOB-REST is that it should be as easy as possible to extend the device model at will. To that end, users may reference their own device-specific Python packages in their configurations files. This section describes how to create and use custom packages.

### Instructions
* Create a Python class to control the device, using whatever scripts and utilities are available to do so.
  * Write the `__init__` method of this class, which will be invoked with the arguments provided by the config file.
  * Write methods in this class for getting and setting any properties you wish to get and set from your device.
  * Create the `config` dictionary before the end of `__init__`. The layout of this dictionary is described below.
* Create a Python package that contains this class, and exposes it via `__init__.py`.
* Install this package on the target system.
* In the server config file, you may now reference the new device class in the new package.

### The `config` Dictionary
The `config` dictionary must be provided so that the server can identify and access the properties of the new device.

The keys of this dictionary are one of:
* `#getter` or `#setter`, which map to instance methods that provide 'get' and 'set' functionality for this property
* `#units`, which maps to a string describing the units used to measure this property
* Strings which identify named properties of the system, and become extensions to the URL route. The mapped values are further `config` dictionaries, allowing the hierarchy to be extended within device classes.

You can think of this dictionary as an extension to the hierarchy modeled by the JSON object in the configuration file. Moreover, the `#obj` tag in the configuration file is merely a directive to "graft the tree" from the new device instance to the server configuration.

### Example: The Random Number Sensor
To help put this all together, here is the full code of a plugin that provides a random floating-point number between the two arguments passed in the configuration file:

```
import random

class RandomNumberSensor(object):
  def __init__(self, lower_bound, upper_bound):
    self.lower = lower_bound
    self.upper = upper_bound
    self.config = {
      'sample': {
        '#getter': self.get_number,
        '#setter': self.set_ranges,
        '#units': 'foobars'
      }
    }

  def get_number(self):
    return random.uniform(self.lower, self.upper)

  def set_ranges(self, ranges):
    self.lower = ranges[0]
    self.upper = ranges[1]

```

If placed in a package called `Example`, this plugin could be instantiated in the configuration file like this:
```
  "randomizer":
    _attach_plugins:
      - module: Example.RandomNumberSensor
        args: [0.0, 1.0]
```
The new random number service can now be accessed at `randomizer/sample`.

### Example: Nested string-storage
To demonstrate the idea that the `config` dictionary merely extends the hierarchy specified by the JSON in the configuration file, here is an example of a plugin that provides read-only strings in a hierarchical way:

```
class StringTree(object):
  def __init__(self):
    self.lower = lower_bound
    self.upper = upper_bound
    self.config = {
      'node1': {
        'node1': {
          '#getter': lambda: 'hello from 1/1'
        },
        'node2': {
          '#getter': lambda: 'hello from 1/2'
        }
      },
      'node2': {
        'node1': {
          '#getter': lambda: 'hello from 2/1'
        },
        'node2': {
          '#getter': lambda: 'hello from 2/2'
        }
      }
    }
```

This produces gettable properties at the URLs `node1/node1`, `node1/node2`, `node2/node1`, and `node2/node2`.

### Caveats with the device class
There are a few caveats that may restrict the design of new device plugins:
* Plugins dictate the privilege level the server must run at; that is, if a plugin requires root access, that plugin forces the server to be run with root access. This should be avoided.
  * It is recommended to add a user that has the necessary privileges to run all the plugins and no extra permissions, and to run the server as that user.
* Plugins must be written such that multiple instances of them may execute concurrently. In practice, this means that device control libraries and scripts used by plugins must support the appropriate atomicity guarantees. Concurrency in this framework is always done with the `threading` library, so plugins may obtain a lock which will be honored by the framework by instantiating a `threading.lock` object in the plugin class' `__init__` method.

## Future Features

### Core Functionality
This section describes changes internal to the server’s code, as opposed to plugins or clients.

#### Asynchronous Operations
Asynchronous operations shall be implemented by supplying a URL argument, named “callback,” where a callback URL shall be given. When this argument is supplied, an HTTP response will be issued immediately, informing the client that the request has been started. Then, when the request is ready, the response that would have been yielded from the request is instead POSTed to the callback URL.

#### Live Reconfiguration with PUT and DELETE
Clients have expressed interest in being able to control the resource tree by sending pieces of a server configuration file to the servers. This can be realized relatively easily, by enabling the PUT and DELETE verbs to invoke the functions for modifying the resource tree based on a given configuration dictionary. These functions already exist, and merely need to be connected to HTTP verbs and tested.

The most likely strategy for implementing the full set of live reconfiguration options through HTTP verbs is to bring the OOB REST service into compliance with the Redfish specification.

#### Server-side Custom Timeouts
Another URL parameter that clients have expressed interest in is a custom request timeout. This will be called “timeout,” and will express a floating-point number of seconds after which the request is dropped by the server and a failure response is yielded. This shall be compatible with the asynchronous operations detailed above in an obvious way. That is, the failure response shall be delivered to the callback URL via POST if the callback is defined.

#### LDAP and OAuth2 Authentication
HTTP Basic Authentication requires that the server store authentication details locally. This does not meet every user’s needs, and some have expressed interest in LDAP integration. An alternative, which seems to be a more progressive option, is to enable OAuth2. The position taken in this document is that both should be implemented, but LDAP should take priority because of its widespread use within Intel (and in customer installations, where Intel engineers need to sign in to obtain red-cover access).

#### Session Management
There is no notion of a user session anywhere in the server as it stands today. This shall be remedied in order to reduce the overhead of separately authenticating a user for each and every HTTP request.

#### Plugin-level User Authorization
The server now has authentication, but no authorization. An authorization system shall be developed, so that users have different levels of access in the system. For example, some plugins may demand a higher level of clearance to use, and certainly ordinary users should not have access to the live reconfiguration services mentioned earlier. This should be implemented in a way that is independent of the chosen authentication strategy.

#### Thread Pool Configuration Options
Currently, all server requests are processed by creating a thread pool to honor the parallel operations of the request concurrently. This should be user-configurable. The server administrator should be able to specify plugins which are to receive their own threads (for long-running plugin methods) and should have control over the number of threads in the pool.

#### Redfish Wrapper
Finally, since the structure of this system is so similar to the Redfish specification, it should be quite straightforward to enable the OData Schema as a configuration option passed to the server.

### Provider Plugins
This section describes the provider plugins that have been identified as necessary to develop for the server to be at all useful.

#### IPMI
Since most commercially-available servers as of the time of this writing have IPMI implementations as their only OOB management scheme, it is necessary to consume all available information from IPMI and provide it in the REST interface.

#### SNMP
Like IPMI, SNMP is a widely used server management system. To use the OOB REST server on such systems, it is necessary to have a provider plugin to OOB that knows how to interact with SNMP.

#### Redfish
Since Redfish is likely successor to IPMI as the de-facto world standard OOB management mechanism, the next-most-important plugin to develop is one which understands Redfish.

#### Redirector
A simple plugin that may have some quality-of-life implications for clients is one which merely redirects to a URL composed of the remaining pieces of a request’s path, aimed at another OOB REST server.

#### Aggregator
An enhancement on the idea of the Redirector plugin is the Aggregator plugin. This plugin will forward the remaining pieces of a request’s path to another OOB REST server, and gathers its response as its result. This enables the concurrency and search functions already in the server to perform an implicit scatter/gather operation across all connected OOB REST servers.

### Front Ends
This section describes a few client applications that could provide useful views of OOB data, and whose development would be made very easy by the REST API.

#### Web GUI
The obvious, straightforward front end to a REST API is a web-browser GUI, where users can explore the resources offered by the API. Hopefully, the “units” offered by the API allow the GUI to provide some rudimentary data visualization, such as real-time live graphs of core temperatures.

#### FUSE FS
The globstar-style search semantics and hierarchical structure of resources lends itself naturally to the implementation of a FUSE daemon, which exposes a sysfs-like tree of OOB information. This tree can even contain symlinks, where redirection and aggregation nodes are, and can implement the “ls” command by merely reading the data provided by non-leaf resource tree nodes.
