# -*- coding: utf-8 -*-


class Request:

    def __init__(self, rtype, operation, address, length=4, data=''):
        self.rtype = rtype
        self.operation = operation
        self.address = address
        self.length = length
        self.data = data


class TraceLine():

    def __init__(self, request, breakpoint = 0):
        self.rtype = request.rtype
        self.operation = request.operation
        self.address = request.address
        self.length = request.length
        self.data = request.data
        print(self.address)
        self.breakpoint = breakpoint


    @classmethod
    def from_string(cls, string):
        # TODO Usar expresion regular https://docs.python.org/2/howto/regex.html para descomponer 'string' en los diferentes campos 
        #      Si hay algún error lanzar excepción para indicarselo al usuario.
        breakpoint = 0
        if 'K' in string:
            breakpoint = string['K']
        rtype = string['F']
        operation = string['T']
        address = int(string['D'], 16)
        length = int(string['Tam'])
        data = string['Dat']
        return cls(Request(rtype, operation, address, length, data), breakpoint)
