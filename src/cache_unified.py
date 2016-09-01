#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from stager import Stager
from cache_viewer import Cache_Viewer
from request import Request
from response import Response
from pycachelib import logging_manager

# Initializing logger
logger = logging_manager.get_logger('')


class Cache_Unified (Stager):

    tags = []
    lines = []

    def __init__(self, configuration):
        super(Cache_Unified, self).__init__(configuration)
        self._name = "Cache_Unified"

        # Inspired in http://www.davidbaldin.com/cache-calculator/
        # Number of bits in the addresses
        self.width = 32
        # Number of bits to address the cache line
        self.index = 4
        # Number of bits to address the byte in the cache line
        self.offset = 8
        # Number of bits in the tag
        self.tag = self.width - (self.index + self.offset)
        # Masks to access the different fields in the address
        self.tag_mask = int(math.pow(2, self.tag) - 1) << (self.index + self.offset)
        self.index_mask = int(math.pow(2, self.index) - 1) << self.offset
        self.offset_mask = int(math.pow(2, self.offset) - 1)

        # Initialize data structures
        self.tags = [-1] * int(math.pow(2, self.index))
        print("tags:")
        print(self.tags)
        self.lines = [0] * int(math.pow(2, self.index))
        print("lines:")
        print(self.lines)

    def stages(self):
        return 3

    def make_viewer(self, parent):
        return Cache_Viewer(parent)

    def exe(self):
        if self.stage == 0:
            # Splitting the address into different fields using the different masks created and bit shifting
            self.tag_part = (self.request.address & self.tag_mask) >> (self.index + self.offset)
            self.index_part = (self.request.address & self.index_mask) >> self.offset
            self.offset_part = (self.request.address & self.offset_mask)
            print "Address fields: " + \
                ('{:0' + str(self.width) + 'b}').format(self.request.address) + " (0x" + \
                ('{:0' + str(self.width / 8) + 'x}').format(self.request.address) + ") = " + \
                ('{:0' + str(self.tag) + 'b}').format(self.tag_part) + " | " + \
                ('{:0' + str(self.index) + 'b}').format(self.index_part) + " | " + \
                ('{:0' + str(self.offset) + 'b}').format(self.offset_part)

            return super(Cache_Unified, self).exe()
        elif self.stage == 1:
            # Search cache default base_address=111111111111
            print("tag mask")
            print(self.tag_mask)
            print("idx mask")
            print(self.index_mask)
            logger.debug("Operations")
            logger.debug("{0} {1} {2} {3} {4}".format(self.request.rtype, self.request.operation, self.request.address, self.request.length, self.request.data))
            print("req add")
            print(self.request.address)
            base_address = self.request.address & (self.tag_mask | self.index_mask)
            print("base add")
            print((self.tag_mask | self.index_mask))
            if self.tags[self.index_part] >= 0 and self.tags[self.index_part] == self.tag_part:
                logger.info("Cache hit")
                self.response = self.lines[self.index_part][self.offset_part]
            else:
                logger.info("Cache miss")
            if self.request.operation == 'L':
                logger.debug("heyy")
                self.up.set_request(Request(self.request.rtype, self. request.operation, base_address, length=int(math.pow(2, self.offset))))
            else:
                logger.debug("nooooope")
                self.up.set_request(Request(self.request.rtype, self.request.operation, self.request.address, length=self.request.length, data=self.request.data))

            return super(Cache_Unified, self).exe()
        else:
            if self.tags[self.index_part] != self.tag_part:
                print "Fetch line from memory"
                # Execute next module in memory hierarchy
                if self.up.exe():
                    # Process response from memory
                    if self.request.operation == 'L':
                        self.response = self.up.get_response()
                        logger.debug(self.lines)
                        self.lines[self.index_part] = self.response.data
                        self.tags[self.index_part] = self.tag_part
                        logger.debug("Response data")
                        logger.debug(self.response.data)
                        logger.debug("Lines")
                        logger.debug(self.lines)
                        logger.debug("index")
                        logger.debug(self.index_part)
                        logger.debug("offset")
                        logger.debug(self.offset_part)
                        self.response.data = self.lines[self.index_part][self.offset_part]
                        logger.debug(self)
                    return super(Cache_Unified, self).exe()
            else:
                return super(Cache_Unified, self).exe()
