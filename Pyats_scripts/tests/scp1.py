import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs_from_file

nr = InitNornir(config_file="config.yaml")

password = getpass.getpass
nr.inventory.defaults.password = password

def scp_push(task):
    task.run(send_configs_from_file, file="scp.txt")

print_result(scp_push)