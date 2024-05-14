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
            command_trip = command.strip()
            
            if command_trip.startswith("export "):
                # "export PATH=$PATH:{BUILD}/compiler/w64devkit/bin"
                # Remove export from command: 
                command_without_export = ((command_trip.split("export"))[1]).strip() # PATH=$PATH:{BUILD}/compiler/w64devkit/bin

                # Get the variable name:
                variable_name = (command_without_export.split("="))[0] # PATH

                # Remove variable name from command
                command_without_export = command_without_export.replace(f'{variable_name}=', "") # $PATH:{BUILD}/compiler/w64devkit/bin

                if f':${variable_name}:' in command_without_export: # in the middle
                    print("in the middle")
                elif f'${variable_name}:' in command_without_export: # in the left
                    remain_command = (command_without_export.split(f'${variable_name}:'))[1] # {BUILD}/compiler/w64devkit/bin
                    os.environ[variable_name] = os.environ[variable_name] + ";" + remain_command
                elif f':${variable_name}' in command_without_export: # in the right
                    remain_command = (command_without_export.split(f':${variable_name}'))[0] # {BUILD}/compiler/w64devkit/bin
                    os.environ[variable_name] = remain_command + ";" + os.environ[variable_name]
                else:
                    os.environ[variable_name] = command_without_export
            else:
                os.system(command)

        os.chdir(cwd)
