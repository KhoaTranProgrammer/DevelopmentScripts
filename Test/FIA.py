import sys
import os
import json
import shutil
import inspect

from Utility import LogInformation
from pathlib import Path

from Test.TestBase import TestBase
from Common import Resource

class FIA(TestBase):
    def __init__(self, json_data):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        TestBase.__init__(self, json_data)

    def execute(self):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])

        for file in self.json_data["Input"]["File"]:
            json_item = {}
            if os.path.exists(file):
                self.createTestItem(self.json_data["Input"]["TestID"], self.json_data["Input"]["Type"], f'File {file} is available', True)
            else:
                self.createTestItem(self.json_data["Input"]["TestID"], self.json_data["Input"]["Type"], f'File {file} is available', False)
