"""Importing from Flask, nornir and nornir_scrapli"""

import getpass
from flask import Flask, render_template
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir.core.filter import F



"""creating the variable app which 
is linked to Flask and __name__"""

app = Flask(__name__)



""" Initialising nornir and prompting user to enter
username and password"""

nr = InitNornir(config_file="config.yaml")
user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password




"""Rendering the homepage using render_template"""

@app.route("/")
def homepage_test():
    return render_template("base.html")



"""Rendering an inventory page and pulling data from the host file"""

@app.route("/hosts/inventory")
def get_all_inventory():
    return render_template("inventory.html", my_list=nr.inventory.hosts.values())



"""Rendering a running configuration page, running the show run command 
and output will be displayed on the running config page"""

@app.route("/all/running")
def get_all_running():
    results = nr.run(task=send_command, command="show run")
    my_list = [v.scrapli_response.result for v in results.values()]
    return render_template("running.html", my_list=my_list)


@app.route("/all/interfaces")
def get_all_interfaces():
    results = nr.run(task=send_command, command="show ip interface brief")
    my_list = [v.scrapli_response.result for v in results.values()]
    return render_template("interfaces.html", my_list=my_list)


@app.route("/all/routes")
def get_all_routes():
    routes = nr.run(task=send_command, command="show ip route")
    my_list = [v.scrapli_response.result for v in routes.values()]
    return render_template("routes.html", my_list=my_list)


@app.route("/hosts/<hostname>/routes")
def get_host_routes(hostname):
    filtered = nr.filter(F(hostname=hostname))
    results = filtered.run(task=send_command, command="show ip route")
    my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template("routes.html", my_list=my_list)


"""Rendering a Device Serial number page, running the show version command 
and output will be displayed, filtering the date using host names and details 
will be shown on the page"""

@app.route("/all/version")
def get_all_version():
    results = nr.run(task=send_command, command="show version")
    my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template("version.html", my_list=my_list)

@app.route("/hosts/<hostname>/version")
def get_host_version(hostname):
    filtered = nr.filter(F(hostname=hostname))
    results = filtered.run(task=send_command, command="show version")
    my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template("version.html", my_list=my_list)



"""running the script using debug mode"""

if __name__ == "__main__":
    app.run(debug=True)
