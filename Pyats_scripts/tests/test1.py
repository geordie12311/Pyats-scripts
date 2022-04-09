from genie.testbed import load

testbed = load("testbed.yaml")

dev = testbed.devices["R1"]
dev.connect(log_stdout=False)
#log)stdout=False will stop Genie outputting the connection data
ip_routes= dev.parse("show ip route")
print(ip_routes)