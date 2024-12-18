import sys
import os
import json
import shutil
import importlib
import inspect

from Utility import LogInformation
from pathlib import Path

from Common.BaseClass import BaseClass
from Common import Resource

class TestCases(BaseClass):
    def __init__(self, json_data):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        BaseClass.__init__(self, json_data)

    def execute(self):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])

        script_dir = Path(os.path.dirname(os.path.abspath(__file__))).as_posix()
        if os.path.exists(os.path.join(script_dir, self.json_data["Input"]["Type"] + ".py")):
            print(f'[TESTTYPE] {self.json_data["Input"]["Type"]} is supported')
            stage = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
            module = importlib.import_module(f'{stage}.{self.json_data["Input"]["Type"]}')
            my_class = getattr(module, f'{self.json_data["Input"]["Type"]}')
            my_instance = my_class(self.json_data)
            my_instance.execute()
        else:
            print(f'[TESTTYPE] {self.json_data["Input"]["Type"]} is NOT supported')
