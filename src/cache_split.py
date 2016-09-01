#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from stager import Stager
from cache_viewer import Cache_Viewer
from cache_unified import Cache_Unified
from request import Request


class Cache_Split (Stager):

    def __init__(self, configuration):
        super(Cache_Split, self).__init__(configuration)
        self._name = "Cache_Split"
        self.inst = Cache_Unified(configuration)
        self.inst._name = self.inst._name + "_Instructions"
        self.data = Cache_Unified(configuration)
        self.data._name = self.data._name + "_Data"

    def connect(self, stager):
        super(Cache_Split, self).connect(stager)
        self.inst.connect(stager)
        self.data.connect(stager)

    def stages(self):
        return 1

    def make_viewer(self, parent):
        splitter = wx.SplitterWindow(parent)
        inst_viewer = self.inst.make_viewer(splitter)
        data_viewer = self.data.make_viewer(splitter)
        splitter.SplitHorizontally(inst_viewer, data_viewer)
        return splitter

    def exe(self):
        if self.stage == 0:
            print "         Dirige peticion"
            if self.request.rtype == 'I':
                self.inst.set_request(self.request)
                if self.inst.exe():
                    return super(Cache_Split, self).exe()
            elif self.request.rtype == 'D':
                self.data.set_request(self.request)
                if self.data.exe():
                    return super(Cache_Split, self).exe()
