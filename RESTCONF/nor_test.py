import requests
import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result
#Result can be used to return the results from restconf back to nornir

"""Initialising nornir, prompting user to enter their credentials
and using getpass to send those creds to each device"""

nr = InitNornir(config_file="config3.yaml")
user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

requests.packages.urllib3.disable_warnings()

headers = {'Accept': 'application/yang-data+json'}


"""Generating the running configurations for all hosts via restconf"""

def restconf_test(task):
    url = f"https://{task.host.hostname}:443/restconf/data/native"
    response = requests.get(url=url, headers=headers, auth=(f"{task.host.username}", f"{task.host.password}"), verify=False)
    return Result(host=task.host, result=response.text)
    #using Result to return the results of the the task back to nornir

results = nr.run(task=restconf_test)
print_result(results)
