"""Python script to enable features on VXLAN nodes"""

import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs_from_file


"""Prompting user for username / password and 
initialising nornir"""

nr = InitNornir(config_file="config.yaml")
user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password


"""Pushing out the features list from txt file"""


def enable_features(task):
    task.run(task=send_configs_from_file, file="basepusher_vxlan.txt")


"""Running the task and printing results"""

results = nr.run(task=enable_features)
print_result(results)
