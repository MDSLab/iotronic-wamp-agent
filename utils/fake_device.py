#! /usr/bin/python
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks, returnValue
from autobahn.twisted.util import sleep

class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("WAMP server session ready!")

        @inlineCallbacks
        def add(x, y):
            c = yield x+y
            returnValue(c)

        @inlineCallbacks
        def hello(client_name, message):
            from random import randrange
            s = randrange(1, 2)
            yield sleep(s)
            result = "Hello by board to Conductor "+client_name+" that told me "+message+" - Time: "+str(s)
            #result = yield "Hello by board to Conductor "+client_name+" that said me "+message
            print "DEVICE result: "+str(result)
		
            returnValue(result)

        try:
            yield self.register(add, u'board.add')
            yield self.register(hello, u'board.hello')
            print("procedures registered")
        except Exception as e:
            print("could not register procedures: {0}".format(e))


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://192.168.17.1:8181/ws", realm=u"s4t")
    runner.run(MyComponent)
