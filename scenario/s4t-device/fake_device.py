from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks, returnValue
#from autobahn.twisted.util import sleep

class MyComponent(ApplicationSession):
  
    @inlineCallbacks
    def onJoin(self, details):
        print("WAMP server session ready!")

<<<<<<< HEAD
	@inlineCallbacks
        def add(x, y):
	    c = yield x+y
            returnValue(c)
	
	@inlineCallbacks
        def hello(client_name, message):
	    from random import randrange
	    #s = randrange(1, 10)
	    #sleep(s)
	    result = yield "Hello by board to Conductor "+client_name+" that said me "+message
=======

        def add(x, y):
            return x+y	
	
        def hello(client_name, message):
	    #print "DEVICE received from WAMP AGENT: "+str(args)
	    result = "Hello by board to Conductor "+client_name+" that said me "+message
>>>>>>> 712f99b9d53304c891ad59b347912238469fe4c8
	    print "DEVICE result: "+str(result)
             
            
            returnValue(result)
	  
        try:
            yield self.register(add, u'com.myapp.add')
            yield self.register(hello, u'com.myapp.hello')
            print("procedures registered")
        except Exception as e:
            print("could not register procedures: {0}".format(e))


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://192.168.17.1:8181/ws", realm=u"s4t")
    runner.run(MyComponent)
    
    
    
    
    