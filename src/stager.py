#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools


class Stager(object):

    def __init__(self, configuration):
        self.stages = self.stages()
        self.stage = 0
        self._name = "noname"

    def stages(self):
        return 5

    def connect(self, stager):
        print "Connecting module " + self._name + " to " + stager._name
        self.up = stager

    def has_next(self):
        return hasattr(self, 'up')

    def set_request(self, request):
        self.request = request

    def get_response(self):
        return self.response

    def exe(self):
        self.stage = self.stage + 1
        print "Executing module " + self._name + " stage " + str(self.stage)
        if self.stage == self.stages:
            # resetting stage index to 0
            self.stage = 0
            return 1
        else:
            return 0
