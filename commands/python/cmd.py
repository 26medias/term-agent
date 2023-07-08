import subprocess
import sys
from langchain.tools import tool

@tool
def execute_python(python_code):
    """
    Execute arbitrary python code

    Parameters:
    - code: The code to execute

    Returns:
    - value of the last line of code
    """
    lines = python_code.split('\n')
    last_line = lines[-1]
    other_lines = lines[:-1]
    python_code = "\n".join(other_lines)
    code_to_execute = f"""
locals_ = {{}}
exec('''
{python_code}
''', globals(), locals_)
print(eval('{last_line}', globals(), locals_))
"""
    result = subprocess.run(['python', '-c', code_to_execute], capture_output=True, text=True, check=True)
    #print("result:", result)
    #print("out:", result.stdout)
    #print("err:", result.stderr, file=sys.stderr)
    try:
        return result.stdout.decode("utf-8")
    except:
        return result.stdout