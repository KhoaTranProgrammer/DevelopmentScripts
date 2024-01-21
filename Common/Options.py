import sys
import os
import json
import shutil
from git import Repo

from Common.BaseClass import BaseClass

class Options(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)
        self.repo = None

    def execute(self):
        cwd = os.getcwd()
        os.chdir(self.json_data["Input"])
        
        for command in self.json_data["Action"]:
            if "export " in command and "PATH=" in command:
                command = (command.split(" PATH="))[1]
                
                if ":$PATH:" in command: # :$PATH: in the middle
                    command = command.split(":$PATH:")
                elif "$PATH:" in command: # $PATH: in the left
                    command = command.split("$PATH:")[1]
                    os.environ['PATH'] = os.environ['PATH'] + ";" + command
                elif ":$PATH" in command: # :$PATH in the right
                    command = command.split(":$PATH")[0]
                    os.environ['PATH'] = command + ";" + os.environ['PATH'] 
            else:
                os.system(command)

        os.chdir(cwd)
