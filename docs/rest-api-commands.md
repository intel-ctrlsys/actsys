## 2.11 Ctrl REST API.

Besides its command line interface, Ctrl also provides a REST-based interface to perform
useful operations in a cluster.

Currently the Ctrl REST API supports only resource and bios subcommands. Other subcommands
will be supported in future versions of Ctrl.

### 2.11.1 Building and Installation.

The REST API is part of the Ctrl package.
Please refer to section [2.1 Building and Installation](2.1-Building-and-Installation.md) from this user guide for general instructions to install it.

### 2.11.2 Configuration Files.

Ctrl REST API exposes the functionality of Ctrl subcommands, so the configuration files described in section [2.2 Configuration Files](2.2-Configuration-Files.md) also apply to propperly set up the REST API.

### 2.11.3 Launching the Ctrl REST API Server.

To get the help menu of the Ctrl REST API execute "`rest_api --help`" command.

```
usage: rest_api [-h] [-V] [-d] [-p PORT] [-H HOST]

Control Rest API

optional arguments:
  -h, --help            shows this help message and exits.
  -V, --version         Provides the tool's version.
  -d, --debug           Enables debug messages.
  -p PORT, --port PORT  Specifies the port to be use for the server
                        application.
  -H HOST, --host HOST  Specifies the host to be use for the server
                        application.

Default values:
    Debug disabled.
    Host: localhost.
    Port: 5000
```


Once the server application has been launched, a rest client program can be used to perform http requests to the server.

#### Example using `curl`:
```bash
curl -i -X GET http://localhost:5000/resource
```

#### Example using python `requests` module:
```python
import requests

def query_resource(url):
    response = requests.get(url)
    return response.status_code

if __name__ == '__main__':
    my_url='http://localhost:5000/resource'
    print query_resource(my_url)
```

Following, a description of the urls for each command supported by the Ctrl REST API will be provided.

#### 2.11.3.1 Resource Commands.

For resource commands to work, the cluster must already have a resource manager running. Also, the local configuration file must specify the resource manager (e.g. SLURM) that is running in the "resource_controller" field. For more information about what the resource commands do, please refer to section [2.5 Resource Commands.](2.5-Resource-Commands.md)

**`Check` subcommand.**

```
HTTP Method: GET
Content Type: JSON
Endpoint: /resource/check
Parameters:
    node_regex  Comma-separated list of nodes to check their status.
Return Codes:
    200  -  Success.
    400  -  Bad Parameter.
    409  -  Could not complete operation.
    404  -  Not found, error.
    424  -  Resource manager not installed.
    207  -  Could not complete operation in one or more nodes.
```

Example:

```bash
curl -i -X GET "http://localhost:5000/resource/check?node_regex=node1,node2,node10"
```

**`Add` subcommand.**

```
HTTP Method: PUT
Content Type: JSON
Endpoint: /resource/add
Parameters:
    node_regex  Comma-separated list of nodes to add to the resource manager.
Return Codes:
    200  -  Success.
    400  -  Bad Parameter.
    409  -  Could not complete operation.
    404  -  Not found, error.
    424  -  Resource manager not installed.
    207  -  Could not complete operation in one or more nodes.
```

Example:

```bash
curl -i -X PUT "http://localhost:5000/resource/add?node_regex=node1,node2,node10"
```

**`Remove` subcommand.**

```
HTTP Method: PUT
Content Type: JSON
Endpoint: /resource/remove
Parameters:
    node_regex  Comma-separated list of nodes to remove from the resource manager.
Return Codes:
    200  -  Success.
    400  -  Bad Parameter.
    409  -  Could not complete operation.
    404  -  Not found, error.
    424  -  Resource manager not installed.
    207  -  Could not complete operation in one or more nodes.
```

Example:

```bash
curl -i -X PUT "http://localhost:5000/resource/remove?node_regex=node1,node2,node10"
```


