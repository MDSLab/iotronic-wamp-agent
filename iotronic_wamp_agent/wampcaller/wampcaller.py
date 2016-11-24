from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor, defer    
import threading
import json


q_forwards = None
q_backwards = None

def printData(d):
    q_backwards.put(d)
    #print "DEVICE sent:",d
    
def printError(failure):
    q_backwards.put(failure)
    print "ERROR "+str(failure)


def wamp_caller(args):
    """thread worker function"""
    print 'WAMP Caller thread started.'
    
    try:
      
	while True:
	  
	  data = q_forwards.get()
	  
	  json_message = json.loads(data)
	  
	  print "--> RPC FUNCTION: "+str(json_message['wamp_rpc_call'])
	  print "--> RPC DATA: "+str(json_message['args'])
	  
	  d = args[0].call(json_message['wamp_rpc_call'],json_message['args'])
	  d.addCallback(printData)
	  d.addErrback(printError)

	
	return
      
    except KeyboardInterrupt:
      print("Stopping WAMP caller")  


# WAMP REACTOR CLASS
class MyComponent(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("WAMP session ready.")
	t = threading.Thread(target=wamp_caller, args=([self],))
	t.start()
        yield "JOINED to WAMP!"

            
    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


class WampCaller(object):
    def __init__(self,qin,qout):
      global q_forwards
      q_forwards = qin
      global q_backwards
      q_backwards = qout
      print "WAMP server starting..."
      self.runner = ApplicationRunner(url=u"ws://192.168.17.1:8181/ws", realm=u"s4t")
      self.runner.run(MyComponent) 
