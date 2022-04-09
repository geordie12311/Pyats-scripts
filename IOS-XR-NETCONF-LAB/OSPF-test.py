#This python script can be used to change any host configuration using a host_var file without Jinja2
#it uses the magic_source python script written by dmitry_figol to convert the yaml host var file to xml
#without having to use complex jinja2 templates

from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result
from lxml import etree
from ruamel.yaml import YAML
from dmitry_figol import magic_sauce
#importing various python libraries and also magic_sauce python script created by dmitry_figol
#Note: do an iniitial grab of the information from the router to create your yaml host_var template
#us onlineyamltools to convert xml to yaml and save your template in the host_vars file. 

def edit_nc_config_from_yaml(task):
    with open(f"host_vars/{task.host}.yaml") as f:
        yaml = YAML(typ="safe")
        data = yaml.load(f)
        xml = magic_sauce.dict_to_xml(data, root="config")
        xml_str = etree.tostring(xml).decode("utf-8")
        result = task.run(task=netconf_edit_config, config=xml_str)
        return Result(host=task.host, result=result.result)
#Function is opening up host_vars folder and grabbing the host.yaml file for each host and assigning it to the variable f.
#Then setting the data as being the yaml file loaded as variable f, using magic_sauce python script to convert the yaml data 
#to xml format and changing the tags to config. and then using etree.tostring to decoede to utf-8 format

def main():
    nr = InitNornir(config_file="config1.yaml")
    results = nr.run(task=edit_nc_config_from_yaml)
    print_result(results)
#function is going to initialise Nornir using config.yaml as config file, run the edit_nc_config_from_yaml function and print results

if __name__ == "__main__":
    main()