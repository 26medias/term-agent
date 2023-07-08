import os
import subprocess
from langchain.tools import tool

@tool
def execute_shell(command):
    """
    Executes an arbitrary shell command.

    Parameters:
    - command: The shell command to execute

    Returns:
    - stdout
    """
    result = subprocess.run([command], capture_output=True, check=True, shell=True)
    return result.stdout.decode("utf-8")
