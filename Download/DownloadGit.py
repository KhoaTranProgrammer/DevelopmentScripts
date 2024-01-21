import sys
import os
import json
import shutil
from git import Repo

from Common.BaseClass import BaseClass

class DownloadGit(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)
        self.repo = None
    
    def execute(self):
        print("This is execute() from DownloadGit: " + str(self.json_data))
        if self.json_data["Action"] == "clone":
            if os.path.exists(self.json_data["Output"]):
                os.system(f'rm -rf {self.json_data["Output"]}')
            os.makedirs(self.json_data["Output"])
            self.repo = Repo.clone_from(self.json_data["Input"]["URL"], self.json_data["Output"])
        elif self.json_data["Action"] == "checkout":
            self.repo = Repo(self.json_data["Output"])
            self.repo.git.execute(["git", "checkout", self.json_data["Input"]["Branch"]])
        else:
            self.repo = Repo(self.json_data["Output"])
            self.repo.git.execute(["git", self.json_data["Action"]])
