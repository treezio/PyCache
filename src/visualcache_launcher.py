# -*- coding: utf-8 -*-

'''
Created on 25/8/2015

@author: Luis Fernandez Tricio
'''
import logging
import os
import sys
import command_interpreter
import trazas_sanitizer
import gui
from pycachelib import logging_manager
from stager import *
from cpu import CPU
from memory import Memory
from cache_unified import Cache_Unified
from cache_split import Cache_Split


"========================="
" Initializing the Logger "
"========================="

# Define the log filename
FILE_NAME = os.path.splitext(os.path.basename(__file__))[0]
# Initialize main logger
logging_manager.init_logger(FILE_NAME)
logger = logging_manager.get_logger()


def create_simulation(configuration):
    '''
    Create the objects for the simulation, based on the specifications of the configuration object.
    The function raises exceptions when the configuration is incorrect.
    @param configuration: Configuration parameters to create the simulation
    @type configuration: Dictionary
    '''
    try:
        # Create the CPU simulator module
        cpu_configuration = configuration['Hardware']['CPU']
        cpu_configuration["TraceFile"] = configuration['TraceFile']
        cpu_module = CPU(cpu_configuration)

        # This will be the first module in the memory hierarchy
        last_module = cpu_module

        # Create the Memory simulator module
        memory_module = Memory(configuration['Hardware']['Memory'])

        # Create the Cache simulator modules
        for module_configuration in configuration['Hardware']:
            if module_configuration == 'CPU':
                logger.debug('There can only be one CPU module')
            elif module_configuration == 'Memory':
                logger.debug('There can only be one Memory module')
            elif module_configuration == 'Cache_Unified':
                next_module = Cache_Unified(module_configuration)
                last_module.connect(next_module)
                last_module = next_module
            elif module_configuration == 'Cache_Split':
                next_module = Cache_Split(module_configuration)
                last_module.connect(next_module)
                last_module = next_module
            else:
                raise Exception("Unknown hardware module {0}".format(module_configuration))

        # Connect the Memory module to the last Cache module
        last_module.connect(memory_module)

    except KeyError as error:
        raise Exception('Configuration error: Key %s not found' % str(error))

    return cpu_module


def main():
    '''
    Main program. Prepares configuration object from different sources (cli,cfg_file,default).
    Creates simulation object structure, from configuration object. Depending on the configuration
    it executes the simulation with or without GUI.
    '''
    logger.info("Visual Cache Launcher Module starting...")
    # Prepare the arguments received from command line
    args_list = []
    for entry in sys.argv[1:]:
        args_list.append(entry)
    logger.debug('Arguments list ready to be sent: {0}'.format(args_list))
    configuration = command_interpreter.main()
    logger.info('Parsed arguments received are: {0}'.format(configuration))

#    trazas_file = initialization_parameters["Memory_Access_Instructions"]
#    trazas_file_path = os.path.join(os.getcwd(),os.path.join("simulation_files",trazas_file))

#    logging.debug("this is the path to the simulation trazas file: {0}".format(trazas_file_path))

#    parsed_instructions = trazas_sanitizer.main(trazas_file_path)
#    logger.debug("Parsed Memory Access Instructions: {0}".format(parsed_instructions))

    # Build simulator objects
    simulation = create_simulation(configuration)

    # Start simulation in gui or in command line mode
    if 'gui' in configuration and configuration['gui'] == '1':
        gui.main(simulation)
    else:
        logger.info("Ejecución continua")
        while not simulation.finished():
            while not simulation.exe():
                1
        logger.debug("Simulation process finished.")

if __name__ == '__main__':
    main()
