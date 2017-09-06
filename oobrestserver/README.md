# OOB-REST
A flexible framework for accessing system management information from the hardware that produces it, and distributing it through a RESTful interface.

## Key Features
* RESTful service for OOB information in JSON
* Parallelism out-of-the-box
* Globstar-style search paths for multiple system properties, also in parallel
* Lightweight (deployable on embedded BMC devices)
* Plugin model for easy extension to new devices
* Configurable system architecture, so you can map your URLs to your system architecture one-to-one
* SSL and HTTP Basic Auth support

## Future Features
* IPMI and Redfish Plugins
* Live reconfiguration with PUT and DELETE
* Content aggregation and redirection
* LDAP and OAuth2 integration
* Asynchronous operations
* Server-side timeout options
* Upgrade to Python 3.4
* Improvements to parallelism performance
* YAML config file support

## Download & Installation
* Clone the repository from css/nc_rest on  [Gerrit](https://sid-gerrit.devtools.intel.com/#/admin/projects/css/nc_rest)
* Navigate to the `server` directory under `nc_rest`
* Run `sudo python setup.py install`

## Running the Test Suite
For each of the three packages shipped with the `nc_rest` repository, the command `py.test` will run the unit tests and BAT tests developed for that package. Run `py.test` from the repository root to execute all of the tests. Installation is not required.

## Startup
Start the OOB-REST server by running `bky-rest`. A configuration file must be provided on the command line; Otherwise, the server will start, but will not actually serve any URLs.

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
To enable SSL, provide the server private key and the certificate file. To enable HTTP basic authorization, provide an "auth file". Auth files contain the hashed passwords and salt values for each username. Auth files can be created or edited with the provided `prototype_auth_edit.py` tool.

## Client API
Clients interact with the OOB-REST server only by issuing one-time HTTP requests to URLs that the server provides. No notion of HTTP session support is provided.

### Valid URL
System properties to be served by OOB-REST are organized in a hierarchical way, as described by the server config file. Therefore, a valid URL route for an instance of the OOB-REST service is a path that identifies some property of the system.

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
--- | ---
`*/a` | `foo/a`, `bar/a`
`*/*/a` | `foo/bar/a`, `bar/foo/a`
`**/a` | `foo/a`, `bar/a`, `foo/bar/a`, `bar/foo/a`

#### URL Parameters
Requests to the OOB-REST server may include URL parameters that configure some of the per-request behavior of the API.

Parameter | Type | Description
-|-|-
`sample_rate` | float | When provided with `duration`, specifies the rate, in Hertz, at which to sample the property.
`duration` | float | When provided with `sample_rate`, specifies the time, in seconds, over which to sample to property.
`timeout` | float | The server shall time out after the provided number of seconds, killing all processes related to the request and returning a failure message to the client. *Note: this argument is not yet implemented, and will be ignored.*
`callback` | string | When provided, a response is given to the client immediately, and the server shall perform a POST operation to the URL provided by this argument when the request is complete. *Note: this argument is not yet implemented, and will be ignored.*

### HTTP methods
The only supported HTTP methods are GET and POST. GET corresponds to the defined "get" behavior of a property, and POST corresponds to the "set" behavior.
> Note: Internally, these map to the methods identified as "#getter" and "#setter" by the plugin configuration dictionary, respectively.

#### GET
The body of any GET request to the OOB-REST server will be ignored. The route and parameters supplied as part of the URL are enough to fully specify a GET request.

#### POST
The body of a POST request should contain only the JSON-serialized object the user wishes to pass as an argument to the setter function of the property identified by the route. The request header must be application/json.

### JSON Response Formats
There are two possible response formats that the OOB-REST server can respond with: directory responses and leaf-node responses.

#### Directory Response
The directory response consists of the key `children` mapped to a JSON object whose keys are the names of URL route pieces that are valid next-level steps down the hierarchy, and whose values are the assembled URLS of those nodes.

### Leaf-node Response
For the response JSON object given by leaf nodes in the hierarchy, the keys are the full route to the property in question and the values are JSON objects with the following schema:

Key | Value Type | Value Description
-|-
`units` | string | A string identifying the units of measurement for this property. It is optional.
`exceptions` | list of strings | List of strings taken by casting any exceptions encountered by plugins during this operation.
`end-time` | float | The server's system time when the operation finished
`start-time` | float | The server's system time when the operation started
`samples` | list of objects | The list of JOSN-serialized objects returned by the plugin as a response for this property. There may be more than one returned object when  the `duration` and `sample_rate` parameters are given.

When multiple properties are identified by an ambiguous path, the response will contain key-value pairs identifying the fully-resolved path and response for each property.

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

## Configuration
To specify the hierarchical structure of data providers that will be reflected in the URLs served by the system, a configuration file must be provided. This file shall be written in a JSON format.

### Basic JSON Structure
The configuration file contains exactly one JSON *object*, where each key is one of the following:
* A URL route piece, in which case the mapped value must be a JSON object specifying the hierarchy beneath it
* The string `#obj`, in which case the mapped value must be a JSON *array* describing the initialization of a leaf node device

### Leaf Node Devices
The JSON *array* used to initialize a device shall have the following form:
* The first element of the array shall be a string that unambiguously identifies a class within a Python package on the system
* The remaining elements of the array, if any, specify the arguments to be given to the class' `__init__` method upon instantiation.

For example, this configuration file section:

```
{
  "foo_string": {
    "#obj": ["DefaultProviders.StringDevice", "foo_file", "Foo"]
  }
}
```

constructs a valid leaf node declaration of the built-in file-backed string-storage device provided with the server package. It will be located at the URL `<host>/foo_string` and will have the initial value `Foo`, by the operation of the class' `__init__` method.

The full definition of all built-in devices is in `server/app/DefaultProviders.py`

### Important Built-in providers
Most of the built-in providers are only useful to the test suite; however, a few devices are provided as utilities available to system architects as they create hierarchies of OOB-REST servers.

#### Built-in Redirection Provider
The provider `DefaultProviders.Redirect` takes one argument during initialization - the remote server to "graft" onto the tree at this location. When a URL routes through this node, the parts of the path after this node will be copied into a new URL which the client will be redirected to. For parallel operations, the ambiguous path provided will not resolve into any properties hosted by the remote node. That is, the nodes under redirection will only appear for single, unambiguous requests.
> This provider has not been implemented yet. A warning and error message will be generated if a configuration file references this provider.

#### Built-in Aggregation Provider
The provider `DefaultProviders.Aggregate` takes one argument during initialization - the remote server to "graft" onto the tree at this location. When a URL routes through this node, the parts of the path after this node will be copied into a new URL for a new request aimed at the remote server. The request will be issued from the server to the remote server, and the response will be copied back to the client. In the case of parallel operations, all responses will be aggregated in one repoly back to the client.
> This provider has not been implemented yet. A warning and error message will be generated if a configuration file references this provider.

#### Performance Notes - Aggregate vs. Redirect
The redirect provider issues more network traffic and does not support parallel operations - so why would a system architecture elect to include it? The reason is server performance. Sometimes, it may be beneficial to provide cross-linking between underpowered devices provided sensor data from the leaves. This redirection node allows this with minimal server overhead, while the aggregation provider requires that the server issue requests and aggregate results.

## Adding Custom Devices
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
{
  "randomizer": {
    #obj': ["Example.RandomNumberSensor", 0.0, 1.0]
  }
}
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
* A plugin instance may not contain state of its own, outside what is provided by `__init__`. This is because the instance will be copied during parallel operations. It is acceptable (and encouraged) that external scripts and files drive the state on a per-request bases.
* Plugins dictate the privilege level the server must run at; that is, if a plugin requires root access, that plugin forces the server to be run with root access. This should be avoided.
  * It is recommended to add a user that has the necessary privileges to run all the plugins and no extra permissions, and to run the server as that user.
* Plugins must be written such that multiple instances of them may execute concurrently. In practice, this means that device control libraries and scripts used by plugins must support the appropriate atomicity guarantees.
