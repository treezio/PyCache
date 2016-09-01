# -*- coding: utf-8 -*-
'''
@name: Command Interpreter Module

This module is able to parse the command Line and store the arguments
in a dictionary, then using those arguments, a new dictionary will be
returned containing the hardware configuration to be used during the
process.

If a specific hardware configuration file is specified by user through
the command line arguments it will be used during the simulation
process. It must contain all the parameters and the must be filled
thought.

Usage:
python command_interpreter.py --arg=value --arg2=value2

The arg keys are the following:

Configuration_File, CPU_Frequency, CPU_Cache, Memory_Size,
Memory_Frequency, Execution_Type, Memory_Access_Instructions

When indicating the units of measure you must not include the unit of
measure but the prefix. (Note: 'M' is for 'Mega' and 'm' for 'mili')

Example:
python command_interpreter.py --Configuration_File=default \
   --Hardware[CPU].Frequency=2G --Hardware[Memory].Size=2000M --ExecutionType=Full

@author: Luis Fernandez Tricio

'''
import sys
import os
from pprint import pprint
from pycachelib.sanitize import sanitize_input_cmdl_format, merge_arg_into_dict, merge_config_dictionaries, invalidInputFormat, invalidInputOption, sanitize_config_file_input
from pycachelib.tools import load_json_into_dictionary, dictionary_routes_parser
from pycachelib import logging_manager

"========================="
" Initializing the Logger "
"========================="

logger = logging_manager.get_logger('')


def how_to_use():
    '''
        This function prints a message that indicates how to use the program
    '''

    htu_message = '''
        Usage:
        python command_interpreter.py --arg=value --arg2=value2

        The arg keys are the following:
        Configuration_File, CPU_Frequency, CPU_Cache, Memory_Size, Memory_Frequency,
        Execution_Type, Memory_Access_Instructions

        Configuration file must have .json extension and must be located at /cfg

        When indicating the units of measure you must not include the unit of measure but the prefix.
        (Note: 'M' is for 'Mega' and 'm' for 'mili')

        Ex:
        python command_interpreter.py --Hardware[CPU].Frequency=2G --Hardware[Memory].Size=2000M --ExecutionType=Full
    '''
    print(htu_message)


def load_config_file_into_dictionary(config_dict):
    '''
    This function creates a dictionary based on the argument list provided

    @param config_dict: Dictionary extracted from configuration file.
    @type config_dict: Dictionary
    '''
    logger.info("Starting config file parsing process...")
    # checking whether the input arguments match the specified RegEx.
    # If they do not match the regex/they are not "-h" or "--help", the process is stopped.
    # Creating aux list, which is necessary for dictionary_routes_parser
    cfg_file_dict = {}
    aux_lst = []
    config_file_input = dictionary_routes_parser(aux_lst, "", config_dict)
    for each_arg in config_file_input:
        try:
            cfg_file_list = sanitize_config_file_input(each_arg)
        except (invalidInputFormat, invalidInputOption):
            how_to_use()
            exit(1)
        cfg_file_dict = merge_arg_into_dict(cfg_file_dict, cfg_file_list)
    return cfg_file_dict


def load_cmdl_into_dictionary(args_list):
    '''
    This function creates a dictionary based on the argument list provided

    @param arg_list: command line arguments
    @type arg_list: List
    '''
    logger.info("Starting command line arguments parsing process...")
    # This is the defaul configuration. Can be overriden by the configuration file and the command line
    input_cmdl_dict = {}
    # checking whether the input arguments match the specified RegEx.
    # If they do not match the regex/they are not "-h" or "--help", the process is stopped.
    for each_argument in args_list:
        # TODO: It is possible to define new default input commands such as --help
        if each_argument == "-h" or each_argument == "--help":
            how_to_use()
            exit(1)
        else:
            # Sanitize argument process
            try:
                input_cmdl_list = sanitize_input_cmdl_format(each_argument)
            except (invalidInputFormat, invalidInputOption):
                how_to_use()
                exit(1)
            # Update Dictionary
            input_cmdl_dict = merge_arg_into_dict(input_cmdl_dict, input_cmdl_list)

    logger.info('These are the parameters parsed from command line: {0} '.format(input_cmdl_dict))
    return input_cmdl_dict


def main():
    '''
    Orchestates the loading of configuration files and merging with the command line parameters

    @param args_list: command line arguments
    @type args_list: String
    '''
    BASE_PATH = os.path.join(os.getcwd(), 'cfg')
    # Main function starts here
    logger.info("Command Interpreter Module starting...")

    # This is the default configuration. Can be overwritten by the configuration file and the command line.
    configuration = {"gui": 1}

    args_list = sys.argv[1:]
    logger.info(args_list)
    # Convert command line parameters into a dictionary. These will later override the configuration read from the configuration file.
    cmdl_configuration = load_cmdl_into_dictionary(args_list)

    # See if a configuration filename has been specified in the command line
    try:
        # looking for a config file input by user.
        config_file_path = cmdl_configuration['ConfigurationFile']
    except KeyError:
        # Default configuration filename
        config_file_path = os.path.join(BASE_PATH, 'pycache_default.json')
    # Load the configuration from the configuration file
    cfg_file_dict = load_json_into_dictionary(config_file_path)

    # Sanitizing config file input
    config_file_dict = load_config_file_into_dictionary(cfg_file_dict)

    # Updating initial configuration dictionary
    # Override configuration with command line parameters
    output_configuration_dict = merge_config_dictionaries(configuration, config_file_dict)
    # Second Merge
    output_configuration_dict = merge_config_dictionaries(output_configuration_dict, cmdl_configuration)

    logger.info("Final Output dict:")
    pprint(output_configuration_dict)
    return output_configuration_dict

if __name__ == '__main__':
    main()
