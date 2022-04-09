from warnings import filters
from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#initialising nornir

def yangsuitetest(task):
    task.run(task=netconf_get_config, source="running", filter_="/native", filter_type="xpath")

results = nr.run(task=yangsuitetest)
print_result(results)