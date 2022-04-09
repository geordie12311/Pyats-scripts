from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

filt = """
<interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
</interfaces>
"""
#creating a filter for operational status of interfaces

def get_device_config(task):
    task.run(task=netconf_get, filter_type="subtree", filter_=filt)
#creating the function to use netconf_get to run the filter and using subtree filter type

results = nr.run(task=get_device_config)
print_result(results)