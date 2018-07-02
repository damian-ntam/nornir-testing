from nornir.core import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result


def basic_configuration(task):
    # Transform inventory data to configuration via a template file

    r = task.run(
        task=text.template_file,
        name="Building basic Configuration",
        template="basic.j2",
        path=f"templates/{task.host.nos}")

    # Save the compiled configuration into a host variable
    task.host["config"] = r.result

    # Deploy that configuration to the device using NAPALM
    task.run(
        task=networking.napalm_configure,
        name="Loading Configuration on the device",
        replace=False,   # False = merge config, True = replace config
        configuration=task.host["config"])


def enable_scp_ios(task):
    r = task.run(
        task=networking.netmiko_send_command,
        name="Loading SCP Configuration on IOS device",
        command_string="configure terminal\n\nip scp server enable\n\nend\n\n")
    return r


nn = InitNornir(config_file="config.yaml", dry_run=False)
# Filter the inventory based on some attributes of devices.
# In this case the 'site' and 'type.'
test_site_devices = nn.filter(site="chiba", type="network_device")
# Filter IOS devices
ios_test_site_devices = nn.filter(site="chiba", nornir_nos="ios")

# Get configuration from IOS devices
ios_config_result = ios_test_site_devices.run(
    task=networking.napalm_get,
    getters=["config"])

# Check the running configuration of IOS devices.
# If not configured for SCP, configure it.
for h, r in ios_config_result.items():
    if "ip scp server enable" not in r.result["config"]["running"]:
        print_title("Playbook to enable SCP on IOS devices at site 'test.'")
        ios_scp_enable_result = ios_test_site_devices.run(task=enable_scp_ios)
        print_result(ios_scp_enable_result)

print_title("Playbook to configure the network devices at site 'test'.")
basic_configuration_result = test_site_devices.run(task=basic_configuration)
print_result(basic_configuration_result)
