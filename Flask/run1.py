from click import command
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")

results = nr.run(task=send_command, command="show ip route")
my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
for data in my_list:
    rprint(data["vrf"]["default"]["address_family"]["ipv4"]["routes"])