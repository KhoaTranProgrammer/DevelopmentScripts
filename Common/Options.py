import sys
import os
import json
import shutil
import inspect

from Common.BaseClass import BaseClass
from Utility import RunCommand
from Utility import ProcessJSON
from Utility import LogInformation

class Options(BaseClass):
    def __init__(self, json_data):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        BaseClass.__init__(self, json_data)
        self.repo = None

    def execute(self):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        cwd = os.getcwd()
        os.chdir(ProcessJSON.ReadJSONData(self.json_data, "Input"))
        
        for command in ProcessJSON.ReadJSONData(self.json_data, "Action"):
            RunCommand.execute_cmd(command)

        os.chdir(cwd)
