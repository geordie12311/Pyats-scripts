# python script to use restconf http plugin to return router-id from hosts
import json
from email import header
from nornir import InitNornir
from nornir_http.tasks import http_method
from nornir_utils.plugins.functions import print_result

# note importing json and also http_method
nr = InitNornir(config_file="config1.yaml")

headers = {"Accept": "application/yang-data+json"}
# creating a header object that will be called by the function below


def pull_restconfig_data(task):
    response = task.run(
        task=http_method,
        method="get",
        verify=False,
        auth=(f"{task.host.username}", f"{task.host.password}"),
        headers=headers,
        url=f"https://{task.host.hostname}:443/restconf/data/native/router",
    )
    task.host["facts"] = json.loads(response.result)
    ospf_rid = task.host["facts"]["Cisco-IOS-XE-native:router"][
        "Cisco-IOS-XE-ospf:router-ospf"
    ]["ospf"]["process-id"][0]["router-id"]
    print(f"{task.host} OSPF router-id is {ospf_rid}")


results = nr.run(task=pull_restconfig_data)
# above function is using http_method to connect via restconf in json format then
# it will parse through the data path using dict and find the ospf router id
# and print out each host name with the associated router-id details
