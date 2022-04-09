#python script using genie to leverage the testbed file from Pyats
#it uses Dq which is a dictionary query library to find key values in the output
from pyats.async_ import pcall
from rich import print as rprint
from genie.testbed import load
from genie.utils import Dq

def get_ospf_routes(hostname, dev):
    parsed = dev.parse("show ip route")
    get_routes = (Dq(parsed).contains("O").get_values("routes"))
    num_routes = len(get_routes)
    rprint(f"{hostname} has {num_routes} OSPF routes in its routing table,\nThese are the routes {get_routes}\n\n")
#the above function is creating an object called get_ospf_routes and then using genie to parse out the output from show ip route.
#It is then using Dq to identify any OSPF routes (using key value "O") and the associated routes. It is then going to print 
# the output for each host showing the number of OSPF routes in the routing table for each host and the route details. 


testbed = load("testbed.yaml")
testbed.connect(log_stdout=False)
results = pcall(get_ospf_routes, hostname=testbed.devices.keys(), dev=testbed.devices.values())

