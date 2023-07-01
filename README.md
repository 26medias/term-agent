# term-agent

A basic agent for the terminal, with modular functions.

## Install

```
cp env.py.example env.py // -> Insert your OPENAI key in env.py
pip install openai
sh install.sh
source ~/.bashrc
```

## Usage

- `hey`: ask anything
- `hey -d` show the debug output
- `hey -r` show the raw unformatted output


## Examples

    $ hey
    > tell me everything you can about my system
    -------------------------
    Your system is running on Linux Alienware-V2 with a version of 5.19.0-45-generic. The system was last updated on Wednesday, June 7, 2023, at 09:08:58 UTC. It is a 64-bit operating system.

-

    $ hey
    > How many days until new year?
    -------------------------
    There are 184 days until the new year.

-

    $ hey
    > how much disk space do I have available?
    -------------------------
    Based on the information provided, the available disk space on your system is as follows:

    - Filesystem: /
    - Total Size: 916G
    - Used: 563G
    - Available: 307G
    - Usage: 65%

    - Filesystem: /boot/efi
    - Total Size: 96M
    - Used: 64M
    - Available: 33M
    - Usage: 67%

    - Filesystem: /media/julien/76E8-CACF
    - Total Size: 977G
    - Used: 65G
    - Available: 912G
    - Usage: 7%

- 

    $ hey
    > Where is conda installed on my system?
    -------------------------
    The conda executable is installed in the following directory on your system:
    /home/julien/anaconda3/bin/conda

- 

    $ hey
    > What are my node & npm versions?
    -------------------------
    The current version of Node is v19.7.0 and the current version of npm is also v19.7.0.