# -*- coding: utf-8 -*-

'''
@name : trazas_sanitizer

This module parses the memory access instructions file returning a list which contains
all the information extracted properly ordered.

@author: Luis Fernandez Tricio
'''
from pycachelib import logging_manager
import re
import os
import csv

"========================="
" Initializing the Logger "
"========================="

logger = logging_manager.get_logger('')


def trazas_sanitizer(trazas_path):
    """
    This function receives the simulation file path as argument
    and checks that it is properly filled.

    @param trazas_path: path to the simulation file.
    @type trazas_path: String
    @return trazas_list: List which contains the lines sanitized
    """
    '''First of all, the memory access instructions is loaded into a list.'''
    trazas_list = []

    trazas_folder = os.path.join(os.getcwd(), "simulation_files")
    try:
        with open(os.path.join(trazas_folder, trazas_path), mode='r') as trazas_lines:
            for line in trazas_lines:
                sub_trazas_list = []
                line = line.strip('\n')
                '''
                #Associated tags:
                Marker: Makes reference to !/# as breakpoint or comment.
                Mode: I or D for Instructions/Data
                MemAdd: HEX value for Memory Address
                Action: L and S for Load/Store
                Size: For data Size in bytes
                Data: As raw data to be processed.
                '''
                logger.debug("Checking whether line {0} meets the requirements or not.".format(str(line)))
                match = re.search(r'^(?P<Marker>[#!]\s)?(?P<Mode>[DF])\s(?P<MemDir>0x[\dA-Fa-f]+)\s(?P<Action>[LS])?(?P<Size>\s\d+)?(?P<Data>\s[^\s]+)?$', str(line))
                if match is None:
                    # TODO: Stops or keeps processing?
                    logger.error('Unable to Match RegEx with line {0}, check that meets the format requirement'.format(str(line)))
                    # raise
                    continue
                else:
                    if match.group('Marker') is None:
                        sub_trazas_list.append('x')
                    else:
                        sub_trazas_list.append(match.group('Marker'))

                    # Adding Mode, MemoryAddress and Action values
                    sub_trazas_list.extend([match.group('Mode'), match.group('MemDir'), match.group('Action')])

                    # Adding Size and Data Values when necessary
                    if match.group('Size') == None or match.group('Data') == None:
                        sub_trazas_list.extend(["", ""])
                    else:
                        sub_trazas_list.extend([match.group('Size'), match.group('Data')])
                logger.debug("Line {0} passed the checking test.".format(line))
                trazas_list.append(sub_trazas_list)
    except IOError as error:
        logger.error(str(error) + " - Simulation File not found, check that Memory_Access_file property is properly filled")

    return trazas_list


def data_sanitizer(trazas_sanitized_list):
    """
    This function receives the simulation file path as argument
    and checks that it is properly filled.

    @param trazas_sanitized_list: List that contains all the data parsed from Simulation File.
    @type trazas_sanitized_list: List
    @return sanitized_data: List that contains the user memory access input.
    @param sanitized_data: List
    """
    '''First of all, the memory access instructions is loaded into a list.'''
    list_small_size = ['K', 'F', 'D', 'T']
    list_big_size = ['K', 'F', 'D', 'T', 'Tam', 'Dat']
    checked_lines = []

    try:
        for idx, input_data in enumerate(trazas_sanitized_list):
            logger.debug("El input_data: {0}".format(input_data))
            if len(input_data) == 6:
                input_data_dict = dict(zip(list_big_size, input_data))
                logger.debug(input_data_dict)
                checked_lines.append(input_data_dict)
            elif len(input_data) == 4:
                input_data_dict = dict(zip(list_small_size, input_data))
                logger.debug(input_data_dict)
                checked_lines.append(input_data_dict)
            else:
                raise Exception("Input data is not properly written in line: {0}".format(idx))
    except Exception as error:
        logger.error(str(error) + " - Input data is not properly written in line: {0}, check that you have filled correctly the Simulation File".format((idx + 1)))
        exit(1)
    try:
        logger.debug(checked_lines)

    except Exception as error:
        logger.error(str(error) + " - unable to identify the input data")

    return checked_lines


def dict_to_csv(data_sanitized_list):
    with open('dict_trazas_sanitized.csv', 'w') as csvfile:
        fieldnames = ['K', 'F', 'D', 'T', 'Tam', 'Dat']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for each_dict in data_sanitized_list:
            writer.writerow(each_dict)


def main(trazas_file_path):

    "==========================="
    " Main function starts here "
    "==========================="

    logger.info("Trazas Sanitizer Module starting...")

    # First of all, the trazas file is sanitized and stored as a list of lists as trazas_sanitized
    trazas_sanitized = trazas_sanitizer(trazas_file_path)
    data_sanitized = data_sanitizer(trazas_sanitized)
    logger.debug("Data Sanitized: {0}".format(data_sanitized))
    # Writing csv file containing the trazas file simulated
    # dict_to_csv(data_sanitized)
    return data_sanitized

if __name__ == '__main__':
    main()
