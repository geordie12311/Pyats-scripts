import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

password = getpass.getpass()
nr.inventory.defaults.password = password

def send_configs(task):
    task.run(task=send_configs_from_file, file="scp.txt")

results = nr.run(task=send_configs)
print_result(results)