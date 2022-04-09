# pyat test to verify that no errors have been reported on network interfaces in the testbed.""
import logging
from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

logger = logging.getLogger(__name__)
# creating a logger for the module


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def load_testbed(self, testbed):
        logger.info(
            "Converting pyATS testbed to Genie testbed to support pyATS Library features"
        )
        testbed = load(testbed)
        self.parent.parameters.update(testbed=testbed)
        # Converts pyATS testbed to Genie Testbed

    @aetest.subsection
    def connect(self, testbed):
        # Make connection to all the devices in testbed. Note: make sure testbed file is in the same directory
        assert testbed, "Testbed is not provided!"
        # Connect to all testbed devices, by default ANY error in the CommonSetup will fail the entire test run
        # Here we catch common exceptions if a device is unavailable to allow test to continue
        try:
            testbed.connect()
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")


class interface_errors(aetest.Testcase):
    counter_error_keys = ("in_crc_errors", "in_errors", "out_errors")
    # List of counters keys to check for errors

    @aetest.setup
    def setup(self, testbed):
        self.learnt_interfaces = {}
        # Learning and saving the interface detials from the devices in the testbed file
        for device_name, device in testbed.devices.items():
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                # Only attempt to learn details on supported network operation systems
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Learning Interfaces for {device_name}")
                self.learnt_interfaces[device_name] = device.learn("interface").info
                # device.learn is used to learn about the interfaces on a device

    @aetest.test
    def test(self, steps):
        for device_name, interfaces in self.learnt_interfaces.items():
            with steps.start(
                f"Looking for Interface Errors on {device_name}", continue_=True
            ) as device_step:
                # Loop over every device with learnt interfaces
                for interface_name, interface in interfaces.items():
                    with device_step.start(
                        f"Checking Interface {interface_name}", continue_=True
                    ) as interface_step:
                        # Loop over every interface that has been learnt
                        if "counters" in interface.keys():
                            # Verify that this interface has "counters" (Loopbacks Lack Counters on some platforms)
                            for counter in self.counter_error_keys:
                                if counter in interface["counters"].keys():
                                    if interface["counters"][counter] > 0:
                                        # Loop over every counter to check, looking for values greater than 0
                                        interface_step.failed(
                                            f'Device {device_name} Interface {interface_name} has a count of {interface["counters"][counter]} for {counter}'
                                        )
                                        # Verify that the counter is available for this device
                                else:
                                    logger.info(
                                        f"Device {device_name} Interface {interface_name} missing {counter}"
                                    )
                                    # if the counter not supported it will log that it wasn't checked
                        else:
                            interface_step.skipped(
                                f"Device {device_name} Interface {interface_name} missing counters"
                            )
                            # If the interface has no counters it will be marked as skipped


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    < common cleanup docstring >
    """

if __name__ == "__main__":
    # for stand-alone execution
    import argparse
    from pyats import topology

    # from genie.conf import Genie

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument(
        "--testbed",
        dest="testbed",
        help="testbed YAML file",
        type=topology.loader.load,
        # type=Genie.init,
        default=None,
    )

    # do the parsing
    args = parser.parse_known_args()[0]

    aetest.main(testbed=args.testbed)