import sys
import os
import json
import argparse
import importlib
import re
from pathlib import Path
from datetime import datetime
from Common import Resource

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

def updateGlobalData(data):
    data = data.replace('{BUILD}', Resource.GLOBAL_VARIABLE["BUILD"])
    data = data.replace('{PATCH}', Resource.GLOBAL_VARIABLE["PATCH"])
    data = data.replace('{PACKAGE}', Resource.GLOBAL_VARIABLE["PACKAGE"])
    data = data.replace('{TEST}', Resource.GLOBAL_VARIABLE["TEST"])
    data = data.replace('{YYYYMMDD}', datetime.today().strftime('%Y%m%d'))
    return data

def updateGlobalVariables(data, variables):
    var_list = variables.split("-")
    for var in var_list:
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
    args = parser.parse_args()

    init()

    # Open and load JSON
    with open(args.json_input) as user_file:
        file_contents = user_file.read()

    file_contents = updateGlobalData(file_contents)
    file_contents = updateGlobalVariables(file_contents, args.variables)

    json_contents = json.loads(file_contents)
    for stage in json_contents:
        if stage in args.stages:
            print(stage)
            if os.path.exists(os.path.join(Resource.GLOBAL_VARIABLE["SCRIPTS"], stage)):
                print(f'[STAGE] Stage {stage} is supported')
                for type in json_contents[stage]:
                    if os.path.exists(os.path.join(Resource.GLOBAL_VARIABLE["SCRIPTS"], stage, stage + type + ".py")):
                        print(f'[TYPE] {type} is supported')
                        for element in json_contents[stage][type]["list"]:
                            module = importlib.import_module(f'{stage}.{stage}{type}')
                            my_class = getattr(module, f'{stage}{type}')
                            my_instance = my_class(element)
                            my_instance.execute()
                    else:
                        if type == "Options":
                            print(f'[TYPE] {type} is supported')
                            for element in json_contents[stage][type]["list"]:
                                module = importlib.import_module(f'Common.{type}')
                                my_class = getattr(module, f'{type}')
                                my_instance = my_class(element)
                                my_instance.execute()
                        else:
                            print(f'[TYPE] {type} is NOT supported')
            else:
                isOptionsSupport = False
                for type in json_contents[stage]:
                    if type == "Options":
                        print(f'[STAGE] Stage {stage} is supported')
                        print(f'[TYPE] {type} is supported')
                        isOptionsSupport = True
                        for element in json_contents[stage][type]["list"]:
                            module = importlib.import_module(f'Common.{type}')
                            my_class = getattr(module, f'{type}')
                            my_instance = my_class(element)
                            my_instance.execute()
                if isOptionsSupport == False:
                    print(f'Stage {stage} is NOT supported')

if main() == False:
    sys.exit(-1)
