import xmltodict
from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get
from nornir_utils.plugins.functions import print_result
from pprint import pprint

# importing xmltodic to convert xml output to dictionary. Also importing netconf_get and pretty print

nr = InitNornir(config_file="config.yaml")
# initialising nornir using config.yaml as config file


def get_yang(task):
    result = task.run(
        task=netconf_get,
        filter_type="xpath",
        filter_="interfaces-state//statistics[in-unicast-pkts > 0]",
    )
    # using netconf to check that the in-unicast-pkts are greater than zero
    output = result.result
    dict_result = xmltodict.parse(output)
    # using xmltodict to reformat the output from get_yang function

    task.host["facts"] = dict_result
    interfaces = task.host["facts"]["rpc-reply"]["data"]["interfaces-state"][
        "interface"
    ]
    for intf in interfaces:
        interface_name = intf["name"]
        print(f"{task.host} {interface_name}'s in-unicast-pkts count greater than zero")
        # filtering the data for each host interface and printing out the result to screen including hostname and interface name


results = nr.run(task=get_yang)
# running the get_yang function
