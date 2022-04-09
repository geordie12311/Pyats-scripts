import json
from pyats.async_ import pcall
from rich import print as rprint
from genie.testbed import load
#note: pcall allows genie to run in parallel

def get_interfaces(dev_name, testbed_value):
    interfaces = testbed_value.parse("show interfaces")
    pretty_int = json.dumps(interfaces, indent=2)
    rprint(f"{dev_name}\n{pretty_int}")
    return interfaces
#function is goin to create an object called get)interfaces and save the output from show interfaces
#it is then going to use json.dumps to clean up the structured data output and indents
testbed = load("testbed.yaml")
testbed.connect(log_stdout=False)
results = pcall(get_interfaces, dev_name=testbed.devices.keys(), testbed_value=testbed.devices.values())
#the above section is creating an object for testbed that is associated to the testbed.yaml file
#it is also going to connect to each device in the testbed file, log_stdout=False hides the connection details
#and finally creating a object called results which will use pcall to run the get_interfaces function in parallel
#and output the device name and the interface details for each device
