import sys
import os
import json

class BaseClass:
    def __init__(self, json_data):
        self.json_data = json_data

    def execute(self):
        print("This is default execute() from BaseClass. It is needed to override")

    def printInfo(self):
        print(self.json_data)
