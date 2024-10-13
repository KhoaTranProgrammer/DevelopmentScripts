import sys
import os
import json
import shutil
from pathlib import Path

from Test.TestBase import TestBase
from Common import Resource

class FIA(TestBase):
    def __init__(self, json_data):
        TestBase.__init__(self, json_data)

    def execute(self):
        print("This is execute() from FIA: " + str(self.json_data))

        for file in self.json_data["Input"]["File"]:
            json_item = {}
            if os.path.exists(file):
                self.createTestItem(self.json_data["Input"]["TestID"], self.json_data["Input"]["Type"], f'File {file} is available', True)
            else:
                self.createTestItem(self.json_data["Input"]["TestID"], self.json_data["Input"]["Type"], f'File {file} is available', False)
