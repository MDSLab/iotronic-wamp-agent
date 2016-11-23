from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor, defer

import threading
from Queue import Queue

from oslo_config import cfg
import oslo_messaging
import logging 
import time
from time import sleep


#import eventlet
#eventlet.monkey_patch()      

q_forwards = Queue()
q_backwards = Queue()
      

def printData(d):
    q_backwards.put(d)
    #print "DEVICE sent:",d
    
def printError(failure):
    q_backwards.put(failure)
    print "ERROR "+str(failure)


def wamp_caller(args):
    """thread worker function"""
    print 'Worker'
    #res = yield self.call(u'com.myapp.hello',["NICOLA"])
    #print("hello call says: {}".format(res))
    #print args[0] + args[1]
    
    #d = defer.Deferred()
    
    while True:
      
      data = q_forwards.get()
      d = args[0].call(u'com.myapp.hello',data)
      d.addCallback(printData)
      d.addErrback(printError)
      
      """
      time.sleep(5)
      print '.'
      d = args[0].call(u'com.myapp.hello',["NICOLA"])
      d.addCallback(printData)
      d.addErrback(printError)
      
      """
    
    return
  


# WAMP REACTOR CLASS
class MyComponent(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("WAMP session ready")
        
	t = threading.Thread(target=wamp_caller, args=([self],))
	threads.append(t)
	t.start()
      
        yield "JOINED to WAMP!"

            
    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


      

# OSLO ENDPOINT for target=test
class TestEndpoint(object):

    def test(self, ctx, arg):
	
	#response = "CONDUCTOR "+arg[0]+" sent: "+ arg[1]
	print "CONDUCTOR sent me: "+str(arg)
	
	q_forwards.put(arg)
	
	while q_backwards.empty():
	  pass
	
	response = q_backwards.get()
	print "DEVICE RPC RESULT: "+str(response)
	return response
	  

      
	

        



# THREAD OSLO SERVER
def oslo_rpc(server):
    """thread worker function"""
    print "AMQP server starting... "

    server.start()
    server.wait()
	
    """
    while True:
      time.sleep(1)
  
    return
    """
  

  
  
threads=[]



 

if __name__ == '__main__':
  
    try:
      
      endpoints = [
	TestEndpoint(),
      ]  
      
      transport_url = 'rabbit://admin:0penstack!@192.168.17.251:5672/'
      transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
      target = oslo_messaging.Target(topic='test', server='server1')     
      
      server = oslo_messaging.get_rpc_server(transport, target, endpoints, executor='blocking')
      
      th = threading.Thread(target=oslo_rpc,args=(server,))
      threads.append(th)
      th.start()

      
      print "WAMP server starting..."
      runner = ApplicationRunner(url=u"ws://192.168.17.251:8080/ws", realm=u"s4t")
      runner.run(MyComponent)

      
    except KeyboardInterrupt:
      print("Stopping server")

