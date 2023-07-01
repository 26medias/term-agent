#!/bin/bash

# Get the directory of the install script
script_dir="$PWD"

# Construct the full path to your Python script
script_path="$script_dir/main.py"

# Add alias to .bashrc
echo "alias hey='python3 $script_path'" >> ~/.bashrc

# Source .bashrc
source ~/.bashrc

echo "Installation completed. You can now use the 'hey' command."
