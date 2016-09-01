'''
PyCache Sanitize Module

This module provides the necessary functions to parse and sanitize the input data

@author: Luis Fernandez Tricio
'''
import re
from collections import MutableMapping
from pycachelib import logging_manager

# initializing logging_manager
logger = logging_manager.get_logger('')


class invalidInputOption(Exception):
    '''
        This class is raised when an invalid input option/flag is detected.
    '''
    def __init__(self, msg=''):
        self.msg = msg
        logger.error(msg)

    def __str__(self):
        return self.msg


class invalidInputFormat(Exception):
    '''
    This class is raised when an invalid input format is detected.
    '''
    def __init__(self, msg=''):
        self.msg = msg
        logger.error(msg)

    def __str__(self):
        return self.msg


def sanitize_single_args(input_key, input_value):
    '''
        This function sanitizes the single_format arguments received from the command line

        @param input_key: input parameter key 'ExecutionType'
        @type input_key: string
        @param input_value: input parameter value. Ex: 'Full'
        @type input_value: string
        @raise invalidInputOption: When key or value parsed from config arguments do not meet the keywords or regex.
        @return: 1
    '''
    # TODO: New keywords could be added if necessary
    allowed_single_keywords = {"input_keys": ["ExecutionType", "TraceFile", "ConfigurationFile"],
                               "input_values": ["Direct", "Step", "Debug"]}

    if input_key in allowed_single_keywords["input_keys"]:
        logger.debug("{0} is an allowed input argument key".format(input_key))
    else:
        raise invalidInputOption("--{0}={1}: Option Error, {0} is not allowed argument key. Check your input configuration.".format(input_key, input_value))

    if input_value in allowed_single_keywords["input_values"] or input_value.endswith('.json') or input_value.endswith('.txt'):
        logger.debug("{0} is an allowed input argument value".format(input_value))
    else:
        raise invalidInputOption("--{0}={1}: Option Error, {1} is not allowed argument value. Check your input configuration.".format(input_key, input_value))
    return 1


def sanitize_complex_args(input_dict_key, input_dict_type, sub_dict_key, input_arg_value):
    '''
        This function sanitizes the single_format arguments received from the command line

        @param input_dict_key: Name of the main key linked to the hardware array. Ex: 'Hardware'
        @type input_dict_key: string
        @param input_dict_type: hardware type key linked to hardware setup. Ex: 'CPU'
        @type input_dict_type: string
        @param sub_dict_key: hardware parameter key. Ex. 'Frequency'
        @type sub_dict_key: string
        @param input_arg_value: hardware parameter value. Ex: 4G
        @type input_arg_value: string
        @raise invalidInputOption: When key or value parsed from config arguments do not meet the keywords or regex
        @return: 1
    '''
    # TODO: New keywords could be added if necessary
    allowed_complex_keywords = {"input_dict_keys": ["Hardware"],
                                "input_dict_types": ["CPU", "Cache_Unified", "Memory", "Cache_Split"],
                                "sub_dict_keys": ["Size", "Frequency"],
                                }

    if input_dict_key in allowed_complex_keywords["input_dict_keys"] and input_dict_type in allowed_complex_keywords["input_dict_types"] and sub_dict_key in allowed_complex_keywords["sub_dict_keys"]:
        logger.debug("{0},{1} and {2} are all allowed input argument keys".format(input_dict_key, input_dict_type, sub_dict_key))
    else:
        raise invalidInputOption("--{0}[{1}].{2}={3}  is not allowed argument. Check your input configuration.".format(input_dict_key, input_dict_type, sub_dict_key, input_arg_value))
    return 1


def merge_config_dictionaries(base_dict, merge_dict):
    '''
        This function merges the different options dictionaries into one.

        @param base_dict: Name of the base dict into which merge_dict will be merged.
        @type base_dict: string
        @param merge_dict: Name of the dictionary which will be merged.
        @type merge_dict: string

    '''
    for k, v in base_dict.iteritems():
        if k in merge_dict:
            # this next check is the only difference!
            if all(isinstance(e, MutableMapping) for e in (v, merge_dict[k])):
                merge_dict[k] = merge_config_dictionaries(v, merge_dict[k])
            # we could further check types and merge as appropriate here.
    output_dict = base_dict.copy()
    output_dict.update(merge_dict)
    return output_dict


def sanitize_config_file_input(cfg_file_arg):
    '''
        This function checks that the input config arguments parsed match the formats.

        @param cmdl_arg: argument received from command line
        @type cmdl_arg: string
        @raise invalidInputFormat: When any received argument does not match the --options format.
        @return: True
    '''
    logger.debug(cfg_file_arg)
    complex_match = re.match(r'^\(\{(?P<input_dict_key>[_a-zA-Z]+)\}\)\(\{(?P<input_dict_type>[_a-zA-Z]+)\}\)\(\{(?P<sub_dict_key>[_a-zA-Z]+)\}\)=\(\{(?P<input_arg_value>[a-zA-Z0-9]+)\}\)$', str(cfg_file_arg))
    single_match = re.match(r'^\(\{(?P<input_key>[_a-zA-Z]+)\}\)=\(\{(?P<input_value>[-_.a-zA-Z0-9]+)\}\)$', str(cfg_file_arg))
    if complex_match is not None:
        input_dict_key = complex_match.group('input_dict_key')
        input_dict_type = complex_match.group('input_dict_type')
        sub_dict_key = complex_match.group('sub_dict_key')
        input_arg_value = complex_match.group('input_arg_value')
        # Sanitizing complex format args
        sanitize_complex_args(input_dict_key, input_dict_type, sub_dict_key, input_arg_value)
        logger.debug("{0} parameter meets the required formatting".format(cfg_file_arg))
        return [input_dict_key, input_dict_type, sub_dict_key, input_arg_value]

    elif single_match is not None:
        input_arg_name = single_match.group('input_key')
        input_arg_value = single_match.group('input_value')
        # Sanitizing single format args
        sanitize_single_args(input_arg_name, input_arg_value)
        logger.debug("{0} parameter meets the required formatting".format(cfg_file_arg))
        return [input_arg_name, input_arg_value]

    else:
        raise invalidInputFormat("Unable to parse configuration file: ERROR {0}".format(cfg_file_arg))


def sanitize_input_cmdl_format(cmdl_arg):
    '''
        This function checks that the input config arguments parsed match the formats.

        @param cmdl_arg: argument received from command line
        @type cmdl_arg: string
        @raise invalidInputFormat: When any received argument does not match the --options format.
        @return: True
    '''
    # flags format --input_arg_name=input_arg_value  Ex: --ExecutionType=4G
    single_match = re.match(r'([-]+)(?P<input_key>[_a-zA-Z]+)[=](?P<input_value>[-_.a-zA-Z0-9]+)', str(cmdl_arg))
    # flags format --input_dict_key[input_dict_type].sub_dict_key=input_arg_value  Ex: --Hardware[CPU].Frequency=4G
    complex_match = re.match(r'^[-]+(?P<input_dict_key>[_a-zA-Z]+)\[(?P<input_dict_type>[_a-zA-Z]+)\]\.(?P<sub_dict_key>[_a-zA-Z]+)[=](?P<input_arg_value>[a-zA-Z0-9]+)$', str(cmdl_arg))
    if single_match is not None:
        input_arg_name = single_match.group('input_key')
        input_arg_value = single_match.group('input_value')
        # Sanitizing single format args
        sanitize_single_args(input_arg_name, input_arg_value)
        logger.debug("{0} parameter meets the required formatting".format(cmdl_arg))
        return [input_arg_name, input_arg_value]
    elif complex_match is not None:
        input_dict_key = complex_match.group('input_dict_key')
        input_dict_type = complex_match.group('input_dict_type')
        sub_dict_key = complex_match.group('sub_dict_key')
        input_arg_value = complex_match.group('input_arg_value')
        # Sanitizing complex format args
        sanitize_complex_args(input_dict_key, input_dict_type, sub_dict_key, input_arg_value)
        logger.debug("{0} parameter meets the required formatting".format(cmdl_arg))
        return [input_dict_key, input_dict_type, sub_dict_key, input_arg_value]
    else:
        raise invalidInputFormat("Unable to parse command line argument {0}, verify that the command line parameters are properly specified".format(cmdl_arg))


def merge_arg_into_dict(config_dict, config_args):
    '''
    This function appends the arguments received into a configuration dictionary

    @param dict: dictionary to be updated
    @type dict: dictionary
    @param config_args: arguments used to be merged into the dictionary
    @type config_args: list of arguments which contain the data to be merged.
    @return: updated dictionary
    '''
    # Splitting in two processes depending on the argument format (2 or 4 parameters in *config_args)
    if len(config_args) == 2:
        # appending to dictionary
        config_dict[config_args[0]] = config_args[1]
        updated_dict = config_dict
    else:
        first_level = {}
        sec_level = {}
        third_level = {}
        # Creating a dictionary out of the parameters parsed: {"[0]":{"[1]":{"[2]":"[3]"}}}
        third_level[config_args[2]] = config_args[3]
        sec_level[config_args[1]] = third_level
        first_level[config_args[0]] = sec_level
        # merging both dictionaries
        updated_dict = merge_config_dictionaries(config_dict, first_level)
    return updated_dict
