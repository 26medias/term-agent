import platform
import os
import json
import glob
import argparse
import importlib.util

from env import OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY

class TermAgent:
    def __init__(self, raw=False, debug=False):
        self.format = raw is False
        self.debug = debug
        self.script_folder = os.path.dirname(os.path.realpath(__file__))
        self.commands, self.functions = self.load_commands()

    # Load the available commands and functions
    def load_commands(self):
        commands = {}
        functions = []
        # Construct the path to the "commands" directory
        commands_dir = os.path.join(self.script_folder, 'commands')
        # Use glob to find all cmd.json files in subdirectories of the "commands" directory
        for filepath in glob.glob(os.path.join(commands_dir, '**', 'cmd.json'), recursive=True):
            with open(filepath, 'r') as file:
                # Load the JSON data
                data = json.load(file)
            # Use the directory path as the key and the data as the value
            directory_path = os.path.dirname(filepath)
            for function_description in data:
                function_name = function_description['name']
                commands[function_name] = {
                    'path': directory_path,
                    'function': function_description
                }
                functions.append(function_description)
        return commands, functions

    # Ask the user what they need, then understand that need using GPT and execute the proper action
    def ask(self):
        user_input = input("> ")
        response = self.ask_gpt(self.wrap(user_input), self.functions)
        parsed, can_format = self.parse(response)
        if parsed is False:
            print("Failed :(")
        else:
            if self.debug:
                print("Answer: ", parsed)
                print("Parse: ", can_format)
            if self.format and can_format:
                if self.debug:
                    print("Formatting the answer:")
                formatted = self.format_response(user_input, parsed)
                return formatted
        return parsed
    
    def sys_info(self):
        system_info = {
            "Operating system name": os.name,
            "Platform system": platform.system(),
            "Platform release": platform.release(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Architecture": platform.architecture(),
            "Uname": platform.uname(),
        }

        if platform.system() == "Windows":
            system_info["Platform specific"] = platform.win32_ver()
        elif platform.system() == "Darwin":
            system_info["Platform specific"] = platform.mac_ver()

        # Generate formatted string
        system_info_str = "\n".join(f"{k}: {v}" for k, v in system_info.items())

        return system_info_str

    # Utility to wrap input for the GPT api
    def wrap(self, input):
        return [{
            "role": "system",
            "content": "You are an AI agent running in the terminal. System info:" + self.sys_info()
        },{
            "role": "user",
            "content": input
        }]

    # Parse a response, executes the required function:
    """
    `response` input example: {
        "content": null,
        "function_call": {
            "arguments": "{\n  \"device\": \"speaker\"\n}",
            "name": "connect_bluetooth"
        },
        "role": "assistant"
    }
    """
    def parse(self, response):
        if self.debug is True:
            print("parse:", response)
        if "function_call" in response:
            fn = response["function_call"]
            name = fn["name"]

            try:
                args = json.loads(fn["arguments"])
            except Exception as e:
                if name == "python":
                    args = {"code": fn["arguments"]}
                else:
                    print("Function call parsing failed:", str(e))
                    return False, False
            try:
                return self.exec(name, args), True
            except Exception as e:
                print("Function call execution failed:", str(e))
                return False, False
        else:
            return response["content"], False
        return True, False
            
    # Exec the required function
    def exec(self, name="", args={}):
        if name in self.commands:
            directory_path = self.commands[name]['path']
            filepath = os.path.join(directory_path, 'cmd.py')
            spec = importlib.util.spec_from_file_location("cmd_module", filepath)
            cmd_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cmd_module)
            return cmd_module.cmd(args)
        else:
            print(f"Unknown command: {name}")
            return False
    

    # Format the output
    def format_response(self, ask, response):
        response = self.ask_gpt([{
            "role": "user",
            "content": ask
        },{
            "role": "system",
            "content": response
        },{
            "role": "user",
            "content": "Please format that answer in a way I can understand"
        }])
        return response["content"]


    # Ask something to GPT agent and get a response, including function to execute
    def ask_gpt(self, chat_messages, functions=None):
        if self.debug:
            print("Sending: ", json.dumps(chat_messages, indent=4))
        try:
            if functions is None:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chat_messages
                )
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=chat_messages,
                    functions=functions
                )
        except Exception as e:
            print("GPT call failed:", str(e))
            return False
        
        return response.choices[0].message



# Set up argument parser
parser = argparse.ArgumentParser(description="Term Agent")
parser.add_argument('-r', '--raw', action='store_true', help='Skip formatting')
parser.add_argument('-d', '--debug', action='store_true', help='Set debug mode')

# Parse arguments
args = parser.parse_args()

# Agent call
agent = TermAgent(raw=args.raw, debug=args.debug)
response = agent.ask()
print("-------------------------")
print(response)