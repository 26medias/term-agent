
import os
import subprocess
import platform
import json
import glob
import argparse

from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

from langchain.tools import tool

from commands.bluetooth.cmd import connect_bluetooth
from commands.file.cmd import write_file
from commands.python.cmd import execute_python
from commands.shell.cmd import execute_shell

class TermAgent:
    def __init__(self, temperature=0):
        tools = [connect_bluetooth, write_file, execute_python, execute_shell]
        memory = ConversationBufferMemory(memory_key="chat_history")
        llm=OpenAI(temperature=temperature)
        self.chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
        self.start()
    
    def start(self):
        response = self.ask()
        print("-------------------------")
        print(response)

    def ask(self):
        user_input = input("> ")
        output = self.chain.run(input=user_input)
        return output




# Set up argument parser
parser = argparse.ArgumentParser(description="Term Agent")
parser.add_argument('-t', '--temperature', help='Skip formatting')

# Parse arguments
args = parser.parse_args()

# Agent call
TermAgent(temperature=args.temperature)