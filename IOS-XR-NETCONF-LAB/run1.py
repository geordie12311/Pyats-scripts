from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

filt = """
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name/>
    <interface>
<interface>
"""
#creating a filter based on the yang module for interface name

def get_device_config(task):
    task.run(task=netconf_get_config, source="running", filter_type="subtree", filter_=filt)
#creating a function to run netconf_get_config to run the filter against running config and filtering by subtree

results = nr.run(task=get_device_config)
print_result(results)