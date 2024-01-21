import sys
import os
import json
import shutil
from git import Repo

from Common.BaseClass import BaseClass

class PatchFiles(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)
        self.repo = None
    
    def execute(self):
        print("This is execute() from PatchFiles: " + str(self.json_data))

        cwd = os.getcwd()
        os.chdir(self.json_data["Output"])

        self.repo = Repo(self.json_data["Output"])
        self.repo.git.execute(["git", "reset", "--hard", "HEAD"])

        for command in self.json_data["Action"]:
            self.repo.git.execute(["git", "apply", self.json_data["Input"] + "/" + command])

        os.chdir(cwd)
