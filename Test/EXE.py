import sys
import os
import json
import shutil
import subprocess
import inspect

from Utility import LogInformation
from pathlib import Path

from Test.TestBase import TestBase
from Common import Resource

class EXE(TestBase):
    def __init__(self, json_data):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        TestBase.__init__(self, json_data)

    def execute(self):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        try:
            if self.json_data["Input"]["SubType"] == "EXE_001": # Check strings contains in output log 
                log = subprocess.run([f'{self.json_data["Input"]["File"]}', f'{self.json_data["Input"]["Arguments"]}'], check=True, capture_output=True, text=True).stdout

                if self.json_data.get('Output'):
                    if self.json_data['Output'].get('CMD_Output'):
                        all_passed = True
                        description = ""
                        for i in self.json_data["Output"]["CMD_Output"]:
                            if i not in log:
                                all_passed = False
                                description = description + f'Could not find "{i}"\n'
                            else:
                                description = description + f'Could find "{i}"\n'
                        self.createTestItem(self.json_data["Input"]["TestID"], self.json_data["Input"]["Type"], description, all_passed)
            elif self.json_data["Input"]["SubType"] == "EXE_002": # Check strings contains in output log can match with expected string in file
                isPASSED = False
                log = subprocess.run([f'{self.json_data["Input"]["File"]}', f'{self.json_data["Input"]["Arguments"]}'], check=True, capture_output=True, text=True).stdout

                if self.json_data.get('Output'):
                    if self.json_data['Output'].get('CMD_Output'):
                        log =log.split("\n")
                        for i in log:
                            if self.json_data["Output"]["CMD_Output"] in i:
                                actual = i.split(self.json_data["Output"]["CMD_Output"])
                                if self.json_data['Input'].get('Expected'):
                                    with open(self.json_data['Input']['Expected']['File']) as expected_file:
                                        file_contents = expected_file.read().splitlines()
                                        for line in file_contents:
                                            if self.json_data['Input']['Expected']['ExpectedData'] in line:
                                                expect =line.split(self.json_data['Input']['Expected']['ExpectedData'])
                                                for k in actual:
                                                    for l in expect:
                                                        if (k == l) and k != "":
                                                            isPASSED = True
                                                            self.createTestItem(self.json_data["Input"]["TestID"], self.json_data["Input"]["Type"], f'{self.json_data["Input"]["Description"]} {k} is correct', isPASSED)
                if isPASSED == False:
                    self.createTestItem(self.json_data["Input"]["TestID"], self.json_data["Input"]["Type"], f'{self.json_data["Input"]["Description"]} can not be found', isPASSED)
        except:
            print("Test case has unexpected issue")
