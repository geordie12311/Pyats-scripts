*** Settings ***
Library   ats.robot.pyATSRobot
Library   unicon.robot.UniconRobot

*** Test Cases ***

Connect to device
    use testbed "testbed.yaml"
    connect to all devices

Execute Useradd Commands
    configure "username test priv 15 password test1" on device "R1"

Disconnect from device
    disconnect from all devices