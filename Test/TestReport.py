import sys
import os
import json
import shutil
import importlib
import inspect

from Utility import LogInformation
from pathlib import Path

from Test.TestBase import TestBase
from Common import Resource

class TestReport(TestBase):
    def __init__(self, json_data):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        TestBase.__init__(self, json_data)

    def execute(self):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        if not os.path.exists(Resource.GLOBAL_VARIABLE["TEST"]):
            os.makedirs(Resource.GLOBAL_VARIABLE["TEST"])

        self.createHtmlReport(f'{self.json_data["Output"]["FileLocation"]}/{self.json_data["Output"]["FileName"]}', Resource.GLOBAL_VARIABLE["TEST_ITEM"])
