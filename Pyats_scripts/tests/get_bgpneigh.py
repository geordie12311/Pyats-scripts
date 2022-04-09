#python script using genie to leverage the testbed file from Pyats
#it uses Dq which is a dictionary query library to find key values in the output
from pyats.async_ import pcall
from rich import print as rprint
from genie.testbed import load
from genie.utils import Dq
#note: pcall allows genie to run in parallel and Dq is a dictionary query that will allow you to find specific data

def get_bgp(hostname, dev):
    output = dev.parse("show bgp neighbors")
    bgp_neigh = output.q.contains("Established").get_values("neighbor")
    rprint(f"{hostname} has these established BGP neighbors{bgp_neigh}.\n\n") 
#the above function is creating an object called get_bgp and then using genie to parse out the output from show bgp neighbors
#It is then using Dq to identify any established connections and the neighbor value. It is then going to print the output for each
#host showing the established neighbor connections. 

testbed = load("testbed.yaml")
testbed.connect(log_stdout=False)
results = pcall(get_bgp, hostname=testbed.devices.keys(), dev=testbed.devices.values())
#creating the object testbed that will use load to load testbed file. Then connecting to the hosts in the testbed file
#Using log_stdout=False to not display connection details on the screen and creating an object called results and using pcall
#to run the gshow bgp neighbors command in parallel across all hosts and associate the hostname and device values that are 
#called upon by the get_bgp function
