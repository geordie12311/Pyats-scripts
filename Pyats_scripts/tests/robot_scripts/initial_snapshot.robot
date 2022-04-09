*** Settings ***
#Importing the test libraries, resource files and variable files

Library   ats.robot.pyATSRobot
Library   unicon.robot.UniconRobot
Library   genie.libs.robot.GenieRobot

*** Variables ***
#Defining the pyATS testbed file for robot to run for this test

${testbed}    testbed.yaml

*** Test Cases ***
#Creating the test cases from keywords

Connect to device
    use testbed "${testbed}"
    connect to device "R1"

Profile the devices
    Profile the system for "bgp;config;interface;platform;ospf;arp;vrf;vlan" on devices "R1" as "./good_snapshot"

Disconnect from device
    disconnect from all devices