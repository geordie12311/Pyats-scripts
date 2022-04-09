#python script using genie to leverage the testbed file from Pyats
#it uses Dq which is a dictionary query library to find key values in the output
from pyats.async_ import pcall
from rich import print as rprint
from genie.testbed import load
from genie.utils import Dq

def get_up_int(hostname, dev):
    parsed = dev.parse("show interfaces")
    oper_up = parsed.q.contains_key_value("oper_status", "up").get_values("[0]")
    oper_down = parsed.q.contains_key_value("oper_status", "down").get_values("[0]")
    rprint(f"{hostname} has these interfaces in that are up{oper_up}.\nAnd these interfaces that are down{oper_down}\n\n") 
#the above function is creating an object called get_up_int and then using genie to parse out the output from show interfaces.
#It is then using Dq to identify any interface with up status and is then going to print the output for each host showing 
#the interfaces on each that are currently up

testbed = load("testbed.yaml")
testbed.connect(log_stdout=False)
results = pcall(get_up_int, hostname=testbed.devices.keys(), dev=testbed.devices.values())
#creating the object testbed that will use load to load testbed file. Then connecting to the hosts in the testbed file
#Using log_stdout=False to not display connection details on the screen and creating an object called results and using pcall
#to run the show interfaces command in parallel across all hosts and associate the hostname and device values that are 
#called upon by the get_up_int function

