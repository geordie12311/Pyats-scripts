import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file


def configure_bgp(task):
    template_to_load = task.run(
        template_file, template=f"{task.host}.j2", path="./templates/bgp_templates"
    )
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="running", config=configuration)
# function is using netconf edit config to replace the ospf running on the hosts with the device specific jinja2 bgp template


def main():
    nr = InitNornir(config_file="config.yaml")
    user = input("Please enter your username: ")
    password = getpass.getpass()
    nr.inventory.defaults.username = user
    nr.inventory.defaults.password = password
    results = nr.run(task=configure_bgp)
    print_result(results)
# function is going to initialise Nornir using config.yaml as config file, run the configure_bgp function and print results
# using getpass to prompt user to input the password which will be used by the script to login to the hosts

if __name__ == "__main__":
    main()
# running the main function to start script
