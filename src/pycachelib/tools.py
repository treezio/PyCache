'''
@name: PyCache Tools Module

This module provides different functions to carry out common tasks.

@author: Luis Fernandez Tricio

'''

from pycachelib import logging_manager
import json

# initializing logging_manager
logger = logging_manager.get_logger('')


def load_json_into_dictionary(json_file_path):
    '''
    This function is able to load a json file into a dictionary.
    @param json_file_path: path to .json file.
    @type json_file: String
    '''
    # Loading the allowed words into a dictionary
    try:
        with open(json_file_path, "r") as dumped_json:
            output_dictionary = json.load(dumped_json)
    except Exception as error:
        logger.error(str(error) + ' - Unable to open and parse configuration file.')
        exit(1)
    return output_dictionary


def dictionary_routes_parser(aux_list, node, routes_dict):
    '''
    This function receives the dict node and the dict itself and returns the node nested route as an ordered list.
    @param aux_list: list to store the arguments parsed in.
    @type aux_list: String
    @param node: Starting node, default root -> ""
    @type node: String
    @param routes_dict: path to .json file.
    @type routes_dict: Dictionary
    @return node_route : list containing all arguments parsed
    '''

    for k, v in routes_dict.iteritems():
        if isinstance(v, dict):
            aux_list = dictionary_routes_parser(aux_list, node + "({" + k + "})", v)
        else:
            aux_list.append(node + "({" + k + "})=({" + v + "})")
    return aux_list
