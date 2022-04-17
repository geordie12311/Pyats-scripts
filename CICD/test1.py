import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def send_random(task):
    task.run(task=send_command, command="show ip int brief")

results = nr.run(task=send_random)
print_result(results)
