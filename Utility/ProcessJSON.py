import sys
import os
import json
import shutil
import subprocess
import hashlib
import re
import inspect

from Utility import LogInformation

def ReadJSONData(json_data, key1, key2=None, key3=None):
    LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
    try:
        if key2 == None:
            return json_data[key1]
        else:
            if key3 == None:
                return json_data[key1][key2]
            else:
                return json_data[key1][key2][key3]
    except:
        LogInformation.LogError(__file__, inspect.stack()[0][3], inspect.stack()[0][2], "Read JSON Data Faile")
