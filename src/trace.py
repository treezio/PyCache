#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

class Trace (object):
    def __init__(self, filename):
        self.f = open(filename, 'r')
        p = re.compile('!?\s*[id]\s+0x[0-9a-f]+\s+[LS](\s+[0-9]+)?(\s+.*)?$', re.IGNORECASE)

        self.line_count = 0
        for line in self.f:
            self.line_count = self.line_count + 1
            trace = line.split('#', 1)[0].rstrip()
            if trace and not trace.isspace() and not p.match(trace):
               print "Syntax error in trace file {0} line {1}: {2} <{3}>".format(filename,self.line_count,line.rstrip(),trace)
        self.reset()

        # Test code
        #lines = self.get_line_count()
        #for i in range(0,lines,2):
        #   sys.stdout.write( self.get_line(i) )
        #sys.stdout.write("---\n")
        #for i in range(lines-1,-1,-2):
        #   sys.stdout.write( self.get_line(i) )

    def reset(self):
        self.f.seek(0, 0)
        self.line_number = -1

    def get_line_count(self):
        return self.line_count

    def get_line(self,line_number):
        if line_number > self.line_number:
           line = self.f.readline()
           while line:
              self.line_number = self.line_number + 1
              if self.line_number == line_number:
                 break
              line = self.f.readline()
           return line
        elif line_number <= self.line_count:
           self.reset()
           return self.get_line(line_number)
        return None
