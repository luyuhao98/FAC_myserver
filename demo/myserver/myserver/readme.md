# Module myserver Reference
- [Module myserver Reference](#module-myserver-reference)
	- [Features](#features)
	- [Terms](#terms)
	- [Member Functions](#member-functions)
		- [\_\_init\_\_(server\_addr,target\_addr=None)](#initserveraddrtargetaddrnone)
		- [connect(addr)](#connectaddr)
		- [group\_connect(target\_addrs)](#groupconnecttargetaddrs)
		- [send(taddr, data)](#sendtaddr-data)
		- [group\_send(group\_num, data)](#groupsendgroupnum-data)
		- [get\_conn(addr)](#getconnaddr)
		- [get\_group\_num(addr)](#getgroupnumaddr)
		- [get\_target\_addrs()](#gettargetaddrs)
		- [get\_server\_addr()](#getserveraddr)
		- [\_func\_map(msg)](#funcmapmsg)
	- [Usage](#usage)
	- [DEMO](#demo)

## Features

1. One new thread for every one-way transmission, such as `accept`, `connect` and `send`.
2. Listens to many clients, sends to many remote hosts.
3. Supports Grouping send
4. Subclass need to override function `_func_map(self,data)`

## Terms
- **server**: a thread, keep on listening, start a new thread for each accepted connections
- **accepted**  the remotes connected to me.
- **connection**: a connection to the target server. One must connect before sending data as a client.
- **target**: target server, alias **remote**
- **group**: indicate the group of remotes. Every `response_info` returned from `_func_map` will be sent to all the sockets in group: `group_num` by `group_send(group_num, data)`. Recommended group numbers: 0 for test, 1 for server, 2 for client.
- **'\n'**: Messages are separated by '\n'.  **Already Packaged. Transparent for `_func_map`**

## Member Functions

### \_\_init\_\_(server\_addr,target\_addr=None)

Public. Init, create a server thread, optionally create client threads.

- `server_addr`: tuple `(server_host,server_port)`. Create a server thread.
	1. `server_host`. e.p. `localhost`,'127.0.0.1'
	2. `server_port`. int,1024-65535
- `target_addr`: 3 choices.
	1. Default None: Do nothing.
	2. tuple `(remote_host,remote_port,group_num)` .Create a client thread to connect to a remote server. And `group_num` indicates which group it is.
	3. list of point2. Create threads to connect to remote servers.

### connect(addr)

Public. Create a client thread to connect to a remote server. If the connection request has been sent or the connection has already been built, it will remind you and then return before doing any other thing.

`addr` : tuple `(remote_host,remote_port,group_num)`
- `remote_host` : string. e.g. 'localhost','127.0.0.1'
- `remote_port` : int. 1024-65535
- `group_num` :  int. Recommendation: 0 for test, 1 for server, 2 for client.

### group\_connect(target\_addrs)

Public. Create client threads to connect to remotes.

`target_addrs`: list of tuple `(remote_host,remote_port,group_num)`

### send(taddr, data)

Public. send data to the target address. If the connection request is not sent to `taddr`, function `send` will remind "Please connect first" and return. If the connection request is sent but has not been connected to `taddr`, it will remind that "Waiting for connection" in a loop which will judge if connected each second. **'\n'  is automatically appended to the end of  the data**

- `taddr` : tuple `(remote_host,remote_port)`
- `data` : string.


### group\_send(group\_num, data)

Public. send data to a group of remotes. Each send will start a new thread. And it will remind 'Group doesn't exist' if there is no such group number

- `group_num`: int
- `data` : str


### get\_conn(addr)
Public. return if the addr is connected

- `addr`: `(remote_host,remote_port)`
- return: False, not connected; True, connected.

### get\_group\_num(addr)
Public. return the addr's group number

- `addr`: `(remote_host,remote_port)`
- return: `group_num`, int

### get\_target\_addrs()
Public. return the remote addresses that we have sent connection request to.

- return：list of tuple:`(remote_host, remote_port)`


### get\_server\_addr()

Public. return the server address

- return: tuple:`(server_host, server_port)`

### \_func\_map(msg)

__Portected and Abstract(MUST INHERIT AND DEFINE HOW TO PROCESS THE DATA SPECIFICALLY). Really Fucking Important__


- `msg`: message received, a stripped string: `\n` has been removed.
- return: Can be None. If not None, the format is tuple:`(response_info,group_num)`
	- `response_info` : string. msg to send. **Watch out: No need for '\n'**
	- `group_num` : int. group to send.

## Usage
1. copy and put module 'myserver' to the path.
2. `from myserver import ms`

## DEMO

click [here](../demo) to see demo.

