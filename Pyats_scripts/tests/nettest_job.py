# pyat job to test connections and test forinterface errors
import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    # run scripts
    run(
        testscript=os.path.join(SCRIPT_PATH, "test_connections.py"),
        runtime=runtime,
        taskid="Device Connections",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "test_interface_errors.py"),
        runtime=runtime,
        taskid="Interface Errors",
    )
