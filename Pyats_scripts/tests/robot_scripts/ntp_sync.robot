*** Settings ***
Library   ats.robot.pyATSRobot
Library   unicon.robot.UniconRobot
Library   genie.libs.robot.GenieRobot

*** Variables ***
#Defining the pyATS testbed file for robot to run for this test

${testbed}    testbed.yaml

*** Test Cases ***

Connect to devices
    use testbed "${testbed}"
    connect to device "R1"

Verify NTP is synchronized on devices
    verify NTP is synchronized on device "R1"

Disconnect from device
    disconnect from all devices