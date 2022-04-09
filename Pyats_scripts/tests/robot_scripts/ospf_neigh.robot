
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

Connect to devices
    use testbed "${testbed}"
    connect to all devices

Verify OSPF Neighbors
    verify count "2" "ospf neighbors" on device "R1"
    verify count "2" "ospf neighbors" on device "R2"   
    verify count "3" "ospf neighbors" on device "R3"
    verify count "3" "ospf neighbors" on device "R4"
    verify count "2" "ospf neighbors" on device "R5"
    verify count "2" "ospf neighbors" on device "R6"
    verify count "3" "ospf neighbors" on device "R7"
    verify count "3" "ospf neighbors" on device "R8"
    verify count "2" "ospf neighbors" on device "CSR1"
    verify count "2" "ospf neighbors" on device "CSR2"

Disconnect from device
    disconnect from all devices