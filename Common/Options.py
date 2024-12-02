import sys
import os
import json
import shutil

from Common.BaseClass import BaseClass
from Utility import RunCommand

class Options(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)
        self.repo = None

    def execute(self):
        cwd = os.getcwd()
        os.chdir(self.json_data["Input"])
        
        for command in self.json_data["Action"]:
            RunCommand.execute_cmd(command)

        os.chdir(cwd)
