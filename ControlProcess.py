import sys
import os
import json
import argparse
import importlib
import re
import inspect

from Utility import LogInformation
from pathlib import Path
from datetime import datetime
from Common import Resource
from Utility import ProcessJSON

global args

def init():
    Resource.GLOBAL_VARIABLE = {}
    Resource.GLOBAL_VARIABLE["SCRIPTS"] = os.path.dirname(os.path.abspath(__file__))
    Resource.GLOBAL_VARIABLE["SCRIPTS"] = Path(Resource.GLOBAL_VARIABLE["SCRIPTS"]).as_posix()

    Resource.GLOBAL_VARIABLE["BUILD"] = os.path.join(os.path.dirname(Resource.GLOBAL_VARIABLE["SCRIPTS"]), "Build")
    Resource.GLOBAL_VARIABLE["BUILD"] = Path(Resource.GLOBAL_VARIABLE["BUILD"]).as_posix()

    Resource.GLOBAL_VARIABLE["DOWNLOAD"] = os.path.join(os.path.dirname(Resource.GLOBAL_VARIABLE["SCRIPTS"]), "Download")
    Resource.GLOBAL_VARIABLE["DOWNLOAD"] = Path(Resource.GLOBAL_VARIABLE["DOWNLOAD"]).as_posix()

    Resource.GLOBAL_VARIABLE["PATCH"] = os.path.join(os.path.dirname(Resource.GLOBAL_VARIABLE["SCRIPTS"]), "Patch")
    Resource.GLOBAL_VARIABLE["PATCH"] = Path(Resource.GLOBAL_VARIABLE["PATCH"]).as_posix()

    Resource.GLOBAL_VARIABLE["PACKAGE"] = os.path.join(os.path.dirname(Resource.GLOBAL_VARIABLE["SCRIPTS"]), "Package")
    Resource.GLOBAL_VARIABLE["PACKAGE"] = Path(Resource.GLOBAL_VARIABLE["PACKAGE"]).as_posix()

    # Use for testing
    Resource.GLOBAL_VARIABLE["TEST"] = os.path.join(os.path.dirname(Resource.GLOBAL_VARIABLE["SCRIPTS"]), "Test")
    Resource.GLOBAL_VARIABLE["TEST"] = Path(Resource.GLOBAL_VARIABLE["TEST"]).as_posix()
    Resource.GLOBAL_VARIABLE["TEST_RESULT"] = True
    Resource.GLOBAL_VARIABLE["TEST_ITEM"] = []

    # Use for log data
    Resource.LOG_DATA = []
    Resource.LOG_LEVEL = args.log

def updateGlobalData(data):
    LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
    data = data.replace('{SCRIPTS}', Resource.GLOBAL_VARIABLE["SCRIPTS"])
    data = data.replace('{BUILD}', Resource.GLOBAL_VARIABLE["BUILD"])
    data = data.replace('{PATCH}', Resource.GLOBAL_VARIABLE["PATCH"])
    data = data.replace('{PACKAGE}', Resource.GLOBAL_VARIABLE["PACKAGE"])
    data = data.replace('{TEST}', Resource.GLOBAL_VARIABLE["TEST"])
    data = data.replace('{YYYYMMDD}', datetime.today().strftime('%Y%m%d'))
    return data

def updateGlobalVariables(data, variables):
    LogInformation.LogFunctionCall(__file__, inspect.stack()[0][3], inspect.stack()[0][2])
    var_list = variables.split("::")
    for var in var_list:
        print(var)
        var = var.split("=")
        name = var[0]
        value = var[1]
        data = data.replace("{" + name + "}", value)
    return data

# Main function
def main():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument("--json_input", "-ji", help="JSON input file that defines steps for processing", default="")
    parser.add_argument("--stages", "-st", help="List of stages to execute", default="ALL")
    parser.add_argument("--variables", "-vars", help="Global variables", default="")
    parser.add_argument("--log", "-lo", help="Log information level", default="0")
    args = parser.parse_args()

    init()

    # Open and load JSON
    with open(args.json_input) as user_file:
        file_contents = user_file.read()

    file_contents = updateGlobalData(file_contents)
    if args.variables:
        file_contents = updateGlobalVariables(file_contents, args.variables)

    json_contents = json.loads(file_contents)
    for stage in json_contents:
        if stage in args.stages or args.stages == "ALL":
            if os.path.exists(os.path.join(Resource.GLOBAL_VARIABLE["SCRIPTS"], stage)):
                LogInformation.LogInformation(__file__, inspect.stack()[0][3], inspect.stack()[0][2], f'[STAGE] Stage {stage} is supported')
                for plugin in ProcessJSON.ReadJSONData(json_contents, stage):
                    if os.path.exists(os.path.join(Resource.GLOBAL_VARIABLE["SCRIPTS"], stage, stage + plugin + ".py")):
                        LogInformation.LogInformation(__file__, inspect.stack()[0][3], inspect.stack()[0][2], f'[PLUGIN] {plugin} is supported')
                        for element in ProcessJSON.ReadJSONData(json_contents, stage, plugin, "list"):
                            module = importlib.import_module(f'{stage}.{stage}{plugin}')
                            my_class = getattr(module, f'{stage}{plugin}')
                            my_instance = my_class(element)
                            my_instance.execute()
                    else:
                        if plugin == "Options" or plugin == "OptionsLoop":
                            LogInformation.LogInformation(__file__, inspect.stack()[0][3], inspect.stack()[0][2], f'[PLUGIN] {plugin} is supported')
                            for element in ProcessJSON.ReadJSONData(json_contents, stage, plugin, "list"):
                                module = importlib.import_module(f'Common.{plugin}')
                                my_class = getattr(module, f'{plugin}')
                                my_instance = my_class(element)
                                my_instance.execute()
                        else:
                            LogInformation.LogInformation(__file__, inspect.stack()[0][3], inspect.stack()[0][2], f'[PLUGIN] {plugin} is NOT supported')
            else:
                isOptionsSupport = False
                for plugin in ProcessJSON.ReadJSONData(json_contents, stage):
                    if plugin == "Options" or plugin == "OptionsLoop":
                        LogInformation.LogInformation(__file__, inspect.stack()[0][3], inspect.stack()[0][2], f'[STAGE] Stage {stage} is supported')
                        LogInformation.LogInformation(__file__, inspect.stack()[0][3], inspect.stack()[0][2], f'[PLUGIN] {plugin} is supported')
                        isOptionsSupport = True
                        for element in ProcessJSON.ReadJSONData(json_contents, stage, plugin, "list"):
                            module = importlib.import_module(f'Common.{plugin}')
                            my_class = getattr(module, f'{plugin}')
                            my_instance = my_class(element)
                            my_instance.execute()
                    elif os.path.exists(os.path.join(Resource.GLOBAL_VARIABLE["SCRIPTS"], plugin + ".py")):
                        LogInformation.LogInformation(__file__, inspect.stack()[0][3], inspect.stack()[0][2], f'[PLUGIN] {plugin} is supported')
                        for element in ProcessJSON.ReadJSONData(json_contents, stage, plugin, "list"):
                            module = importlib.import_module(f'{plugin.replace("/", ".")}')
                            my_class = getattr(module, f'{plugin.split("/")[-1]}')
                            my_instance = my_class(element)
                            my_instance.execute()
                if isOptionsSupport == False:
                    LogInformation.LogInformation(__file__, inspect.stack()[0][3], inspect.stack()[0][2], f'Stage {stage} is NOT supported')

    print(Resource.LOG_DATA)

if main() == False:
    sys.exit(-1)
