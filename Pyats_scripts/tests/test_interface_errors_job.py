"""
test_interface_errors_job.py

Verify that no errors have been reported on network interfaces in the testbed.

"""
import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    """job file entrypoint"""

    # run script
    run(testscript=os.path.join(SCRIPT_PATH, "test_interface_errors.py"), runtime=runtime)