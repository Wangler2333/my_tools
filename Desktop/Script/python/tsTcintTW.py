#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou

from twisted.internet import protocol, reactor

HOST = 'localhost'
PORT = 21569

class TSCintProtocol(protocol.Protocol):
    def sendData(self):
        data = raw_input('> ')
        if data:
            print '... sending %s...' % data
            self.transport.write(data)
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data):
        print data
        self.sendData()

class TSCintFactory(protocol.ClientFactory):
    protocol = TSCintProtocol
    clientConnectionLost = clientConnectionFailed = lambda self, connector, reason: reactor.stop()


reactor.connectTCP(HOST, PORT, TSCintFactory())
reactor.run()