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

class TestBase(BaseClass):
    def __init__(self, json_data):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        BaseClass.__init__(self, json_data)

    def createTestItem(self, testID, type, description, result):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        if result == True:
            test_item = {"Output": {"TestID": testID, "Type": type, "Description": description, "Result": "PASSED"}}
        else:
            Resource.GLOBAL_VARIABLE["TEST_RESULT"] = False
            test_item = {"Output": {"TestID": testID, "Type": type, "Description": description, "Result": "FAILED"}}
        Resource.GLOBAL_VARIABLE["TEST_ITEM"].append(test_item)

    def createHtmlReport(self, htmlFile, testItems):
        LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
        # to open/create a new html file in the write mode 
        f = open(htmlFile, 'w')
        f.write("<table>\n")
        f.write("<tr>\n")
        f.write("<th>TestID</th>\n")
        f.write("<th>Type</th>\n")
        f.write("<th>Description</th>\n")
        f.write("<th>Result</th>\n")
        f.write("</tr>\n")

        for item in testItems:
            f.write("<tr>\n")
            f.write(f'<td>{item["Output"]["TestID"]}</td>\n')
            f.write(f'<td>{item["Output"]["Type"]}</td>\n')

            description = (item["Output"]["Description"]).replace("\n", "<br>")
            f.write(f'<td>{description}</td>\n')

            f.write(f'<td>{item["Output"]["Result"]}</td>\n')
            f.write("</tr>\n")

        f.write("</table>")

        # close the file
        f.close()
