import sys
import os
import json
import shutil
import subprocess
import hashlib
import re

from Common import Resource

# Type:
#   + CAL: function call
def LogFunctionCall(file, function, line):
    if Resource.LOG_LEVEL != "0":
        Resource.LOG_DATA.append(f'[CAL] - [FILE]{file} - [FUNCTION]{function} - [LINE]{line}')

# Type:
#   + LOG: information
#   + ERR: error
def LogInformation(file, function, line, infor):
    if Resource.LOG_LEVEL != "0":
        Resource.LOG_DATA.append(f'[LOG] - [FILE]{file} - [FUNCTION]{function} - [LINE]{line} - [INFOR]{infor}')

# Type:
#   + ERR: error
def LogError(file, function, line, infor):
    if Resource.LOG_LEVEL != "0":
        Resource.LOG_DATA.append(f'[ERR] - [FILE]{file} - [FUNCTION]{function} - [LINE]{line} - [INFOR]{infor}')
