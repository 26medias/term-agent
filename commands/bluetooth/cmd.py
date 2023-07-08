import os
import subprocess
from langchain.tools import tool

@tool
def connect_bluetooth(device):
    """
    Connect to a bluetooth device

    Parameters:
    - device: headphones | speaker

    Returns:
    - bluetoothctl connect stdout
    """
    script_name = f'connect-{device}.sh'
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    result = subprocess.run(['sh ' + script_path], capture_output=True, check=True, shell=True)
    return result.stdout.decode("utf-8")
