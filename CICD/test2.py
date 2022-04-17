from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError

nr = InitNornir(config_file="config.yaml")

def configs(task):
    task.run(task=send_configs_from_file, file="configtest.txt")

results = nr.run(configs)
print_result(results)
failures = nr.data.failed_hosts
if failures:
    raise NornirExecutionError("Nornir Failure Detected")
