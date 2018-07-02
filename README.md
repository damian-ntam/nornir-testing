# nornir-testing
Playing with nornir.

Working through the [tutorial](https://nornir.readthedocs.io/en/latest/tutorials/intro/overview.html) in the Nornir docs.

## nornir-test1
This follows along with the first half of the tutorial in the docs with some added operations. A weird issue I had working on the device_audit task: if multiple remote_commands were sent in the task, Paramiko would error out with an EOF error or a SSH session not active error. I started to debug it but found that NAPLM getters could provide what I was after.

## nornir-test2
This follows along with the second half of the tutorial in the docs. I tested deploying configuration to a IOS-XE and NXOS. If you're using IOS or IOS-XE, the plugin Nornir uses is NAPALM which uses netmiko as a driver. SCP server must be enabled for configuration operations to work (_ip scp server enable_). I added an SCP validation and configuration task to handle this.