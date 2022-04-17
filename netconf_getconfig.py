import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config1.yaml")

user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

def get_config(task):
    task.run(task=netconf_get_config, source="running", filter_="/native", filter_type="xpath")

results = nr.run(task=get_config)
print_result(results)