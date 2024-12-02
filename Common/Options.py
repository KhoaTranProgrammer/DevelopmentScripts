import sys
import os
import json
import shutil

from Common.BaseClass import BaseClass
from Utility import RunCommand
from Utility import ProcessJSON

class Options(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)
        self.repo = None

    def execute(self):
        cwd = os.getcwd()
        os.chdir(ProcessJSON.ReadJSONData(self.json_data, "Input"))
        
        for command in ProcessJSON.ReadJSONData(self.json_data, "Action"):
            RunCommand.execute_cmd(command)

        os.chdir(cwd)
