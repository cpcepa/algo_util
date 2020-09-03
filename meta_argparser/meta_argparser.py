'''
module          : meta_argparser.py
function        : Online parsing of meta.yaml to generate the parameters
                  to read in.
                  Supports all as: catch-all

Changelog       : 0.1- initial release
Date modified   : 02/09/2020
version         : 0.1
'''

import argparse
import yaml
import json
from ast import literal_eval as make_tuple


def catch_all(value):
    try:
        converted_value = json.loads(value)
        return converted_value
    except json.decoder.JSONDecodeError:
        pass
    try:
        converted_value = make_tuple(value)
        return converted_value
    except (ValueError, SyntaxError):
        pass

    return value  # a string, hopefully


def str2type(v):
    # dictionary for type, more for I/O files
    type_dict = {
        "string": str,
        "int": int,
        "float": float,
        "None": None,
        "catch-all": catch_all,
        "bool": bool,
    }
    if v in type_dict:
        return type_dict[v]
    else:
        return v


def read_arg(arg_types_list):
    """
    Function: interpret "oneOf" of the meta
    input: arg_name, arg_typesList, index of current param
    return: string to be written to py
    """
    # for arg.py
    curr_type = arg_types_list[0]
    arg_default = curr_type["default"]
    if arg_default == "None":  # proper convert None
        arg_default = None
    arg_type = catch_all

    return arg_type, arg_default


def parse_yaml(meta_yaml_path="../meta.yaml"):

    with open(meta_yaml_path, "r") as file:
        meta = yaml.full_load(file)

    CLI = argparse.ArgumentParser()
    # for the I/O and parameters
    input_present = True
    output_present = True
    param_present = True

    try:
        inputs = meta["inputs"]
    except KeyError:
        print("no inputs in meta.yaml")
        input_present = False

    try:
        parameters = meta["parameters"]
    except KeyError:
        print("no parameter in meta.yaml")
        param_present = False

    try:
        outputs = meta["outputs"]
    except KeyError:
        print("no outputs in meta.yaml")
        output_present = False

    if input_present:
        for index in range(len(inputs)):
            arg = inputs[index]
            arg_name = "--" + arg["name"]
            arg_types_list = arg["oneOf"]  # oneOf is a list of dicts
            curr_type = arg_types_list[0]  # since there is only 1
            arg_type = str2type(curr_type["type"])
            arg_default = curr_type["default"]
            CLI.add_argument(arg_name, type=arg_type, default=arg_default)

    if output_present:
        for index in range(len(outputs)):
            arg = outputs[index]
            arg_name = "--" + arg["name"]
            arg_types_list = arg["oneOf"]  # oneOf is a list of dicts
            curr_type = arg_types_list[0]  # since there is only 1
            arg_type = str2type(curr_type["type"])
            arg_default = curr_type["default"]
            CLI.add_argument(arg_name, type=arg_type, default=arg_default)

    param_list = []  # for creating a param_list later
    if param_present:
        for index in range(len(parameters)):
            arg = parameters[index]
            arg_name = arg["name"]
            arg_name_cmd = "--" + arg_name
            arg_types_list = arg["oneOf"]  # oneOf is a list of dicts
            arg_type, arg_default = read_arg(arg_types_list)
            CLI.add_argument(arg_name_cmd, type=arg_type, default=arg_default)
            param_list.append(arg_name)

    args = CLI.parse_args()
    # insert testing fuction here

    # isolate the algo parameters
    algo_parameters = {}
    for parameter in param_list:
        algo_parameters[parameter] = getattr(args, parameter)
        # print(type(algo_parameters[parameter]), parameter)

    return args, algo_parameters
