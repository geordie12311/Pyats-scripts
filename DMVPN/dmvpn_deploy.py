import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file


def load_vars(task):
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["facts"] = data.result
    group_data = task.run(task=load_yaml, file="./group_vars/all.yaml")
    task.host["group_facts"] = group_data.result
    config_vrf(task)


# This function is loading the group variables into memory, also starting config_vrf task


def config_vrf(task):
    vrf_template = task.run(
        task=template_file,
        name="Buildling VRF Configuration",
        template="vrf.j2",
        path="./templates",
    )
    task.host["vrf"] = vrf_template.result
    vrf_output = task.host["vrf"]
    vrf_send = vrf_output.splitlines()
    task.run(task=send_configs, name="Pushing VRF Commands", configs=vrf_send)
    config_dmvpn(task)


# This function is generating the VRF template and pushing out the config, also staring config_dmvpn task


def config_dmvpn(task):
    dmvpn_template = task.run(
        task=template_file,
        name="Buildling DMVPN Configuration",
        template="dmvpn.j2",
        path="./templates",
    )
    task.host["dmvpn"] = dmvpn_template.result
    dmvpn_output = task.host["dmvpn"]
    dmvpn_send = dmvpn_output.splitlines()
    task.run(
        task=send_configs,
        name="Pushing DMVPN Commands",
        configs=dmvpn_send,
    )
    config_bgp(task)


# This function is generating the DMVPN template and pushing out the config, also staring config_bgp task


def config_bgp(task):
    bgp_template = task.run(
        task=template_file,
        name="Buildling BGP Configuration",
        template="bgp_dmvpn.j2",
        path="./templates",
    )
    task.host["bgp"] = bgp_template.result
    bgp_output = task.host["bgp"]
    bgp_send = bgp_output.splitlines()
    task.run(task=send_configs, name="Pushing BGP Commands", configs=bgp_send)


# This fuction is generating the BGP template and pushing out the configuration


def main():
    nr = InitNornir(config_file="config.yaml")
    user = input("Please enter your username: ")
    password = getpass.getpass()
    nr.inventory.defaults.username = user
    nr.inventory.defaults.password = password
    filtered = nr.filter(dmvpn="yes")
    results = filtered.run(task=load_vars)
    print_result(results)


# function is going to initialise Nornir using config2.yaml as config file, run the load_vars function and print results
# using getpass to prompt user to input the password which will be used by the script to login to the hosts

if __name__ == "__main__":
    main()
# running the main function to start script
