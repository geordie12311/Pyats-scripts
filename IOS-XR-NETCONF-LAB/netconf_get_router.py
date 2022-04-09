import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result


def get_device_config(task):
    task.run(
        task=netconf_get_config,
        source="running",
        filter_type="xpath",
        filter_="/native/router",
    )

def main():
    nr = InitNornir(config_file="config1.yaml")
    user = input("Please enter your username: ")
    password = getpass.getpass()
    nr.inventory.defaults.username = user
    nr.inventory.defaults.password = password
    results = nr.run(task=get_device_config)
    print_result(results)
#function is going to initialise Nornir using config.yaml as config file, run the edit_nc_config_from_yaml function and print results
#using getpass to prompt user to input the password which will be used by the script to login to the hosts

if __name__ == "__main__":
    main()
#running the main function to start script
