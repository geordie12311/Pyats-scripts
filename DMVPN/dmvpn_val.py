"""Python script to automatically build DMVPN 
Configuration using Restconf. Script will validate
the configuration and if any errors discard the changes"""

import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import (
    send_configs,
    netconf_lock,
    netconf_validate,
    netconf_commit,
    netconf_discard,
    netconf_unlock,
)
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file


"""Loading the host var files into memory"""

def load_vars(task):
    data = task.run(
        task=load_yaml,
        name="Loading Vars into Memory...",
        file=f"./host_vars/{task.host}.yaml",
    )
    group_data = task.run(task=load_yaml, file="./group_vars/all.yaml")
    task.host["facts"] = data.result
    task.host["group_facts"] = group_data.result


"""Locking the candidate configurations"""

def lock_config(task):
    task.run(task=netconf_lock, target="candidate", name="Locking Candidate Config...")
    # config_vrf(task)


"""Generating the VRF configuration"""

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


"""Generating the DMVPN tunnels"""

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


"""Generating the BGP configuration"""

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


"""Validating the candidate configs"""

def validate_configs(task):
    task.run(task=netconf_validate, source="candidate")


"""committing the configs"""

def commit_configs(task):
    task.run(
        task=netconf_commit, name="Committing Changes into Running Configuration..."
    )


"""Discarding configs if any errors are found"""

def discard_all(task):
    task.run(task=netconf_discard, name="Discarding uncommitted changes....")


"""Unlocking the candidate config files"""

def unlock_config(task):
    task.run(task=netconf_unlock, name="Unlocking Candidate configs....")


"""Running the main script functions"""

def main():
    nr = InitNornir(config_file="config.yaml")
    user = input("Please enter your username: ")
    password = getpass.getpass()
    nr.inventory.defaults.username = user
    nr.inventory.defaults.password = password

    vars_results = nr.run(task=load_vars)
    print_result(vars_results)

    vrf_results = nr.run(task=config_vrf)
    print_result(vrf_results)

    bgp_results = nr.run(task=config_bgp)
    print_result(bgp_results)

    dmvpn_results = nr.run(task=config_dmvpn)
    print_result(dmvpn_results)
 
    commits = nr.run(task=commit_configs)

    validate_results = nr.run(task=validate_configs)
    print_result(validate_results)
    failures = nr.data.failed_hosts
    if failures:
        undo_all = nr.run(task=discard_all)
    else:
        commits = nr.run(task=commit_configs)
    print_result(undo_all)

    unlocker = nr.run(task=unlock_config, name="NETCONF_UNLOCK")
    print_result(unlocker)
 
if __name__ == "__main__":
    main()
