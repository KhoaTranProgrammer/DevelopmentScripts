import sys
import os
import json
import shutil
import importlib
from pathlib import Path

from Test.TestBase import TestBase
from Common import Resource

class TestReport(TestBase):
    def __init__(self, json_data):
        TestBase.__init__(self, json_data)

    def execute(self):
        print("This is execute() from TestResult: " + str(self.json_data))
        if not os.path.exists(Resource.GLOBAL_VARIABLE["TEST"]):
            os.makedirs(Resource.GLOBAL_VARIABLE["TEST"])

        self.createHtmlReport(f'{self.json_data["Output"]["FileLocation"]}/{self.json_data["Output"]["FileName"]}', Resource.GLOBAL_VARIABLE["TEST_ITEM"])
