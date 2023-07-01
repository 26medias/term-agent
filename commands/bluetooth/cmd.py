import os
import subprocess

def cmd(params={}):
    script_name = f'connect-{params["device"]}.sh'
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    result = subprocess.run(['sh ' + script_path], capture_output=True, check=True, shell=True)
    return result.stdout.decode("utf-8")
