*** Settings ***
#Importing the test libraries, resource files and variable files

Library   ats.robot.pyATSRobot
Library   genie.libs.robot.GenieRobot

*** Variables ***
#Defining the pyATS testbed file for robot to run for this test

${testbed}    testbed.yaml

*** Test Cases ***
#Creating the test cases from keywords

Connect to devices
    use testbed "${testbed}"
    connect to all devices

Profile the devices
    Profile the system for "bgp;config;interface;platform;ospf;vrf;arp;vlan" on devices "R1" as "./new_snapshot"

Compare snapshots
    Compare profile "./initial_snapshot" with "./new_snapshot" on devices "R1"

Disconnect from device
    disconnect from all devices