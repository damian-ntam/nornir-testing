from nornir.core import InitNornir
from nornir.plugins.tasks import commands, networking
from nornir.plugins.functions.text import print_result
import logging

def device_audit(task):
    task.run(task=networking.napalm_get, name="Device Interfaces", getters=["interfaces"])
    task.run(task=networking.napalm_get, name="Device Environment", getters=["environment"])
    task.run(task=networking.napalm_get, name="Device Users", getters=["users"])

host_inv = InitNornir(config_file="config.yaml")

test_hosts = host_inv.filter(site="test", role="access")

rmcmd_result = test_hosts.run(task=commands.remote_command, command="dir")
print_result(rmcmd_result, vars=["stdout"])

napalm_result = test_hosts.run(task=networking.napalm_get,getters=["facts"])
print_result(napalm_result)

task_result = test_hosts.run(task=device_audit)
print_result(task_result)