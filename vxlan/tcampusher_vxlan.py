"""Python script to push out tcam settings to VXLAN nodes"""

import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs_from_file
from nornir.core.filter import F


"""Prompting user for username / password and 
initialising nornir"""

nr = InitNornir(config_file="config.yaml")
user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password


"""Pushing out the tcam setting from txt file"""


def push_tcam(task):
    task.run(task=send_configs_from_file, file="leaf-tcam.txt")


"""Filtering hosts for Leaf only and runningg
the push_tcam task. Printing results"""

filtered = nr.filter(F(layer="Leaf"))
tcam_results = filtered.run(task=push_tcam)
print_result(tcam_results)
