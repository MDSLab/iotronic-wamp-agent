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
import json



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
	threads.append(t)
	t.start()
      
        yield "JOINED to WAMP!"

            
    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


      

# OSLO ENDPOINT for target=test
class WampEndpoint(object):

    def s4t_invoke_wamp(self, ctx, arg):

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

    try:
      
	server.start()
	server.wait()
	
    except KeyboardInterrupt:
      print("Stopping OSLO server")

  

  
  
threads=[]



 

if __name__ == '__main__':
  
    try:
      
      endpoints = [
	WampEndpoint(),
      ]  
      
      transport_url = 'rabbit://openstack:0penstack@192.168.17.1:5672/'
      transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
      target = oslo_messaging.Target(topic='s4t_invoke_wamp', server='server1')     
      
      server = oslo_messaging.get_rpc_server(transport, target, endpoints, executor='blocking')
      
      th = threading.Thread(target=oslo_rpc,args=(server,))
      threads.append(th)
      th.start()

      
      print "WAMP server starting..."
      runner = ApplicationRunner(url=u"ws://192.168.17.1:8181/ws", realm=u"s4t")
      runner.run(MyComponent)

      
    except KeyboardInterrupt:
      print("Stopping WAMP-agent server")

