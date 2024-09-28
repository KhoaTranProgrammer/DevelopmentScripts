import sys
import os
import json
import shutil

from Common.BaseClass import BaseClass

class Description(BaseClass):
    def __init__(self, json_data):
        BaseClass.__init__(self, json_data)
