from nornir.core import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result
from nornir.plugins.tasks.files import write_file

init_nornir = InitNornir(config_file="config.yaml", dry_run=True)
test_site_devices = init_nornir.filter(site="test", type="network_device")

def basic_configuration(task):
    # Transform inventory data to configuration via a template file
    r = task.run(task=text.template_file,
                 name="Base Configuration",
                 template="basic.j2",
                 path=f"templates/{task.host.nos}")

    # Save the compiled configuration into a host variable
    task.host["config"] = r.result

    # Deploy that configuration to the device using NAPALM
    task.run(task=networking.napalm_configure,
             name="Loading Configuration on the device",
             replace=False,
             configuration=task.host["config"])

print_title("Playbook to configure the network devices at site test.")
result = test_site_devices.run(task=basic_configuration)
print_result(result)