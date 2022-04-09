"""
test_connections_job.py
Verify that all devices in the testbed can be successfully connected to.
"""
import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    """job file entrypoint"""

    # run script
    run(testscript=os.path.join(SCRIPT_PATH, "test_connections.py"), runtime=runtime)