#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import izip_longest
from stager import Stager
from request import Request
from response import Response
from memoryviewer import MemoryViewer
from pycachelib import logging_manager

# Initializing logger
logger = logging_manager.get_logger('')


class Memory (Stager):

    memory = {}

    def __init__(self, configuration):
        super(Memory, self).__init__(configuration)
        self._name = "Memory"

    def stages(self):
        return 1

    def make_viewer(self, parent):
        self.gui = MemoryViewer(parent)
        return self.gui

    def read(self, address):
        # Offset is 8 by default
        segment = str(address >> 8)
        logger.debug("Main Memory")
        logger.debug(self.memory)
        logger.debug("Segment")
        logger.debug(segment)

        logger.debug(address & 0xff)
        # If address is stored as memory dict, its values is returned.
        if not hasattr(self.memory, segment):
            logger.debug("has not")
            return 0
        logger.debug("data")
        logger.debug(self.memory[segment][address & 0xff])
        return self.memory[segment][address & 0xff]

    def write(self, address, data):
        segment = str(address >> 8)
        if segment not in self.memory:
            self.memory[segment] = [0] * (2**8)
        self.memory[segment][address & 0xff] = data
        self.segment_to_string(address)

    def segment_to_string(self, address):
        segment = str(address >> 8)
        args = [iter(self.memory[segment])] * (2**4)
        return hex((address >> 8) << 8) + ':\n' + '\n'.join([' '.join(['{:2}'.format(item) for item in row])
            for row in izip_longest(*args, fillvalue=11)])

    def exe(self):
        self.response = Response(self.request)
        if self.stage == 0:
            if self.request.operation == 'L':
                logger.debug("load")
                for address in range(self.request.address, self.request.address + self.request.length):
                    self.response.data.append(self.read(address))
            elif self.request.operation == 'S':
                logger.debug("Store")
                if self.request.data:
                    for address in range(self.request.address, self.request.address + self.request.length):
                        self.write(address, self.request.data[address - self.request.address])
                    if hasattr(self, 'gui'):
                        # TODO: Maybe not use clearAll and print all segments.
                        self.gui.pnl2.ClearAll()
                        self.gui.pnl2.AppendText(self.segment_to_string(address))
        return super(Memory, self).exe()
