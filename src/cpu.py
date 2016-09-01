#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stager import Stager
import trazas_sanitizer
from cpu_viewer import CPU_Viewer
from request import Request, TraceLine


class CPU (Stager):

    def __init__(self, configuration):
        super(CPU, self).__init__(configuration)
        self._name = "CPU"
        for key in configuration:
            if key == 'TraceFile':
                self.trace_file = configuration['TraceFile']
        self.open_trace()

    def open_trace(self):
        try:
            # Check trace file for syntax errors
            self.trace = trazas_sanitizer.main(self.trace_file)
            # Set trace pointer to first event in the trace
            self.line = 0
        except AttributeError:
            raise Exception("The CPU module does not have a TraceFile")

    def stages(self):
        return 2

    def finished(self):
        # Return true if there is no more events in the trace file
        if hasattr(self, 'gui'):
            return self.line == self.gui.get_line_count()
        else:
            return self.line == len(self.trace)

    def make_viewer(self, parent):
        self.gui = CPU_Viewer(parent, self)
        self.trace = ''
        return self.gui

    def reset(self):
        self.line = 0

    def get_next_request(self):
        if hasattr(self, 'gui'):
            return self.gui.get_line(self.line)
        else:
            return self.trace[self.line]

    def exe(self):
        if self.stage == 0:
            # Read load/store event from trace file and send up the memory hierarchy
            print "Sending request to " + self.up._name
            self.up.set_request(TraceLine.from_string(self.get_next_request()))
        #          self.up.set_request(Request(self.get_next_request()))
        #          self.up.set_request(Request('S',0,length=1,data=[30]))
        #          self.up.set_request(Request('S',16,length=1,data=[31]))
        #          self.up.set_request(Request('S',8,length=1,data=[32]))
        #          self.up.set_request(Request('S',255,length=1,data=[33]))
        #          self.up.set_request(Request('D','S',16,length=4,data=[33,34,35,36]))
        #          self.up.set_request(Request('I','L',0x00001233))
            # returning stage position
            return super(CPU, self).exe()
        else:
            # Execute next module in memory hierarchy
            if self.up.exe():
                # If next module has finished processing, increment trace pointer
                self.line = self.line + 1
                return super(CPU, self).exe()
