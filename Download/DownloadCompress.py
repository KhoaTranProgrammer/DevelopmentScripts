import sys
import os
import json
import shutil
import wget
import zipfile

from Common.BaseClass import BaseClass
from Common import Resource

class DownloadCompress(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)
        self.repo = None
    
    def execute(self):
        print("This is execute() from DownloadCompress: " + str(self.json_data))
        if not os.path.exists(Resource.GLOBAL_VARIABLE["DOWNLOAD"]):
            os.makedirs(Resource.GLOBAL_VARIABLE["DOWNLOAD"])

        filename = os.path.basename(self.json_data["Input"]["URL"])
        filetype = (filename.split("."))[-1]
        localfilepath = os.path.join(Resource.GLOBAL_VARIABLE["DOWNLOAD"], filename)

        # Check and remove if file exist
        if os.path.exists(localfilepath):
            os.remove(localfilepath)

        if os.path.exists(self.json_data["Output"]):
            os.system(f'rm -rf {self.json_data["Output"]}')
        os.makedirs(self.json_data["Output"])

        # Download file into download folder
        wget.download(self.json_data["Input"]["URL"], Resource.GLOBAL_VARIABLE["DOWNLOAD"])

        # Extract to output location
        if filetype.lower() == "zip":
            with zipfile.ZipFile(localfilepath, "r") as zip_ref:
                zip_ref.extractall(self.json_data["Output"])

        if ".7z.exe" in filename.lower():
            os.system(f'{localfilepath} -o"{self.json_data["Output"]}" -y')

        if self.json_data.get("Action") != None:
            for command in self.json_data["Action"]:
                os.system(command)
