from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor, defer


from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted import wamp, websocket
from autobahn.wamp import types


import threading
from Queue import Queue

from oslo_config import cfg
import oslo_messaging

import logging 
import time
from time import sleep
import json
import uuid

from concurrent.futures import ThreadPoolExecutor
global pool
pool = ThreadPoolExecutor(3) #pool == executor

from oslo_log import log

LOG = log.getLogger(__name__)

#import eventlet
#eventlet.monkey_patch()      

q_forwards = Queue()
q_backwards = Queue()
      
threads=[]

test=None

global DB_THR
DB_THR={}




def printD(d, uuid):

    print uuid
    DB_THR[uuid]['result']=d
    print "DEVICE sent:",DB_THR[uuid]['result']
    
    


def printE(failure):
    print "ERROR "+str(failure)      




def wamp_request(req_uuid, kwarg,session):
  
    def printD(d):
      #q_backwards.put(d)
      global DB_THR
      DB_THR[req_uuid]['result']=d
      print "DEVICE sent:",d
      return DB_THR[req_uuid]['result']
      
    def printE(failure):
      #q_backwards.put(failure)
      global DB_THR
      DB_THR[req_uuid]['result']=failure
      print "ERROR "+str(failure)
      
    
    
    global test
    d = session.wamp_session.call(test, kwarg['wamp_rpc_call'],*kwarg['data'])
    d.addCallback(printD)	      
    d.addErrback(printE)



# OSLO ENDPOINT for target=test
class WampEndpoint(object):
    
    def __init__(self,wamp_session):
        self.wamp_session=wamp_session

    def s4t_invoke_wamp(self, ctx, **kwarg):

	print "CONDUCTOR sent me:",kwarg
	req_uuid = uuid.uuid4()
	DB_THR[req_uuid]={}
	DB_THR[req_uuid]['result']=None
	
	th = threading.Thread(target=wamp_request,args=(req_uuid, kwarg,self))
	threads.append(th)
	th.start()


        while DB_THR[req_uuid]['result'] == None:
          pass

	print DB_THR[req_uuid]['result']
	
	return  DB_THR[req_uuid]['result']


        



# THREAD OSLO SERVER
def oslo_rpc(server):
    """thread worker function"""
    print "AMQP server starting... "

    try:
	server.start()
	server.wait()
	
    except KeyboardInterrupt:
      print("Stopping OSLO server")

  

  
  







class MyFrontendComponent(wamp.ApplicationSession):
    
    def onJoin(self, details):
        global test
        test=self
	print("WAMP session ready.")


    def onDisconnect(self):
	print("disconnected")
        reactor.stop()


class MyClientFactory(websocket.WampWebSocketClientFactory, ReconnectingClientFactory):
    maxDelay = 30

    def clientConnectionFailed(self, connector, reason):
        print "*************************************"
        print "Connection Failed"
        print "reason:", reason
        print "*************************************"
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print "*************************************"
        print "Connection Lost"
        print "reason:", reason
        print "*************************************"
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)



 

if __name__ == '__main__':
  
    try:
        
      # WAMP CONFIG
      
      ## 1) create a WAMP application session factory
      component_config = types.ComponentConfig(realm = u"s4t")
      session_factory = wamp.ApplicationSessionFactory(config = component_config)
      session_factory.session = MyFrontendComponent
      
      ## 2) create a WAMP-over-WebSocket transport client factory
      transport_factory = MyClientFactory(session_factory)
      
      ## 3) start the client from a Twisted endpoint
      transport_factory.host = '192.168.17.1'
      transport_factory.port = 8181
      websocket.connectWS(transport_factory)  
        
        
      # AMQP CONFIG
      endpoints = [
	WampEndpoint(MyFrontendComponent),
      ]  
      
      transport_url = 'rabbit://openstack:0penstack@192.168.17.1:5672/'
      transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
      target = oslo_messaging.Target(topic='s4t_invoke_wamp', server='server1')     
      
      server = oslo_messaging.get_rpc_server(transport, target, endpoints, executor='threading')
      
      ## 4) now enter the Twisted reactor loop
      print "REACTOR starting..."
      
      
      th = threading.Thread(target=oslo_rpc, args=(server,))
      threads.append(th)
      th.start()

      
      print "WAMP server starting..."
      

      reactor.run()
      
    except KeyboardInterrupt:
      print("Stopping WAMP-agent server")

