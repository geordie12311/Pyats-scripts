"""Python Script to automatically build fabric on VLXAN for Nexus platform.
Scrip will also clean up configuration / lockdown unused ports afterwards"""

import getpass
import json
import logging
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs, send_commands_from_file, send_command
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.functions import print_result


"""Initialising nornir, prompting for password"""

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password

"""Sending out the base configuration to the hosts"""


def push_base_config(task):
    task.run(task=send_commands_from_file, file="basepush_vxlan.txt")
    load_vars(task)


"""Generating the host var files and loading in memory"""


def load_vars(task):
    loader = task.run(task=load_yaml, file=f"host_vars/{task.host}.yaml")
    task.host["facts"] = loader.result
    push_ospf(task)


"""Generating the OSPF configuration using jinja2 template"""


def push_ospf(task):
    template = task.run(task=template_file, template="ospf.j2", path="templates")
    task.host["ospf_config"] = template.result
    rendered = task.host["ospf_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)
    push_bgp(task)


"""Generating the BGP configuration using jinja2 template"""


def push_bgp(task):
    template = task.run(task=template_file, template="bgp.j2", path="templates")
    task.host["bgp_config"] = template.result
    rendered = task.host["bgp_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)
    get_cdp(task)


"""Collating the CDP neighbor information. non Management or Loopback
interfaces will be appended to the interface_list"""


def get_cdp(task):
    interfaces_list = []
    interfaces_result = task.run(
        task=send_command,
        command="show interface brief | json",
        severity_level=logging.DEBUG,
    )
    task.host["interfaces_facts"] = json.loads(interfaces_result.result)
    interfaces = task.host["interface_facts"]["TABLE_interface"]["ROW_interface"]
    for interface in interfaces:
        intf = interface["interface"]
        if intf not in ("mgmt0", "loopback0"):
            interfaces_list.append(intf)

    cdp_result = task.run(task=send_command, command="show cdp neighbor | json")
    severity_level = (logging.DEBUG,)
    task.host["cdp_facts"] = json.loads(cdp_result.result)
    connections = task.host["cdp_facts"]["TABLE_cdp_neighbor_brief_info"][
        "ROW_cdp_neighbor_brief_info"
    ]

    for device in connections:
        platform = device["platform_id"]
        if platform == "N9K-9000v":
            local_intf = device["intf_id"]
            interfaces_list.remove(local_intf)
    clean_interfaces(task, interfaces_list)


"""Using the interface_list to set unused interfaces 
as switchports and shutting them down"""


def clean_interfaces(task, interfaces_list):
    for interface in interfaces_list:
        task.run(
            task=send_configs,
            configs=[
                f"interface {interface}",
                "switchport",
                "shutdown",
                "description SHUTDOWN",
            ],
        )


results = nr.run(task=push_base_config)
print_result(results)
