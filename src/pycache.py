# -*- coding: utf-8 -*-

import logging
import os
import sys
import confargparse
import gui
from stager import *
from cpu import CPU
from memory import Memory
from cache_unified import Cache_Unified
from cache_split import Cache_Split

# Maximum number of cache levels that the simulator can handle
max_levels = 3

# set up logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(levelname)s - %(message)s')
logger = logging.getLogger('')

def load_configuration():
    parser = confargparse.ConfArgParser()

    #parser.add_argument("-c", help='Defines de CPU frequency.')
    parser.add_argument("-t", help='Defines trace file.')
    parser.add_argument("-g", help='Use GUI.', action='store_true')

    for level in range(1,max_levels+1):
        parser.add_argument("-i{0}".format(level), help='Definition of level {0} instruction cache.'.format(level))
        parser.add_argument("-d{0}".format(level), help='Definition of level {0} data cache.'.format(level))
        parser.add_argument("-u{0}".format(level), help='Definition of level {0} unified cache.'.format(level))

    args = parser.parse_args()
    args_vars = vars(args)

    last_level = 1
    for level in range(1,max_levels+1):
        u = "u{0}".format(level)
        i = "i{0}".format(level)
        d = "d{0}".format(level)

        if args_vars.get(u) and ( args_vars.get(d) or args_vars.get(i)):
            parser.error("-{0} can not be specified with -{1} or -{2}.".format(u,i,d))
        if args_vars.get(i) and args_vars.get(d) is None or args_vars.get(d) and args_vars.get(i) is None:
            parser.error("-{0} and -{1} must be specified together.".format(i,d))
        if args_vars.get(i) is None and args_vars.get(d) is None and args_vars.get(u) is None:
            last_level = 0
        else:
            if last_level == 0:
                parser.error("Can't specify cache level {0} without specifying the previous one.".format(level))
            last_level = 1
    return args_vars   

def create_simulation(configuration):
    '''
    Create the objects for the simulation, based on the specifications of the configuration object.
    The function rises exceptions when the configuration is incorrect.
    @param configuration: Configuration parameters to create the simulation
    @type configuration: Dictionary   
    '''

    # Create the CPU simulator module 
    cpu_module = CPU(configuration)
    # This will be the first module in the memory hierarchy
    last_module = cpu_module

    # Create the Memory simulator module
    memory_module = Memory(configuration)

    # Create the Cache simulator modules
    for level in range(1,max_levels+1):
        if configuration.get("u{0}".format(level)):
            next_module = Cache_Unified(configuration,level)
            last_module.connect(next_module)
            last_module = next_module
        elif configuration.get("i{0}".format(level)) and configuration.get("d{0}".format(level)):
            next_module = Cache_Split(configuration,level)
            last_module.connect(next_module)
            last_module = next_module

    # Connect the Memory module to the last Cache module
    last_module.connect(memory_module)
    return cpu_module

def main():
    '''
    Main program. Prepares configuration object from different sources (cli,cfg_file,default).
    Creates simulation object structure, from configuration object. Depending on the configuration
    it executes the simulation with or without GUI.
    '''
    logger.debug("PyCache starting...")  
    configuration = load_configuration()
    
    # Build simulator objects
    simulation = create_simulation(configuration)

    # Start simulation in gui or in command line mode
    if configuration.get("g"):
       gui.main(simulation)
    else:
        logger.debug("Starting full execution.")
        module = simulation
        module.reset_statistics()
        while module.has_next():
            module = module.up
            module.reset_statistics()

        while not simulation.finished():
            while not simulation.exe():
                1

        module = simulation
        module.print_statistics()
        while module.has_next():
            module = module.up
            module.print_statistics()
        logger.debug("End of full execution.")
    
if __name__ == '__main__':
    main()
