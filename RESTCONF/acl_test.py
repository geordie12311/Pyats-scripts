import getpass
import requests
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir.core.task import Result

"""initialising nornir, prompting user
for username / password and using getpass to
send details to hosts"""

nr = InitNornir(config_file="config4.yaml")
user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password


"""Disabling the url warnings and setting the headers / chained_url links"""

requests.packages.urllib3.disable_warnings()

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}
chained_url = "data/openconfig-acl:acl"


"""Generating the host var file data and loading into memory"""


def load_data(task):
    data = task.run(task=load_yaml, file=f"host_vars/{task.host}.yaml")
    task.host["facts"] = data.result


"""Generating the data from the host file to put to the hosts
via restconf"""


def configure_data(task, chained_url, headers):
    restconf_url = f"https://{task.host.hostname}:443/restconf/"

    response = requests.put(
        url=restconf_url + chained_url,
        headers=headers,
        auth=(f"{task.host.username}", f"{task.host.password}"),
        verify=False,
        json=task.host["facts"]["configure_acl"],
    )

    return Result(host=task.host, result=response.text)


"""running the tasks "load_data" and configure_data
and printing the outupt to the screen"""

load_results = nr.run(task=load_data)
print_result(load_results)
configure_results = nr.run(configure_data, chained_url=chained_url, headers=headers)
print_result(configure_results)
