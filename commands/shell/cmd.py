import os
import subprocess

def cmd(params={}):
    result = subprocess.run([params["command"]], capture_output=True, check=True, shell=True)
    return result.stdout.decode("utf-8")
