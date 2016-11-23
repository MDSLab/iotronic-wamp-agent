from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks
from time import sleep

class MyComponent(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("WAMP server session ready!")

        def add2(args):
	    sleep(1)
            return args[0] + args[1]

        def hello(args):
	    from random import randrange
	    #s = randrange(1, 10)
	    #sleep(1)
	    print "DEVICE received from WAMP AGENT: "+str(args)
	    
	    result = "Hello by board to Conductor "+args[0]+" that said me "+args[1]
	    
	    print "DEVICE result: "+str(result)
            return result
	  
        try:
            yield self.register(add2, u'com.myapp.add2')
            yield self.register(hello, u'com.myapp.hello')
            print("procedures registered")
        except Exception as e:
            print("could not register procedures: {0}".format(e))


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://192.168.17.251:8080/ws", realm=u"s4t")
    runner.run(MyComponent)