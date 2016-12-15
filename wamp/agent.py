from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor, defer


from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted import wamp, websocket
from autobahn.wamp import types


import threading
from threading import Thread

import oslo_messaging

from oslo_config import cfg
from oslo_log import log as logging


LOG = logging.getLogger(__name__)
CONF = cfg.CONF
CONF.debug=True

DOMAIN = "scenario"
logging.register_options(CONF)
logging.setup(CONF, DOMAIN)


shared_result={}
wamp_session_caller=None


def wamp_request(e, kwarg,session):
    
    id=threading.current_thread().ident
    shared_result[id]={}
    shared_result[id]['result']=None
  
    def success(d):
      shared_result[id]['result']=d
      LOG.debug( "DEVICE sent: %s", str(d))
      e.set()
      return shared_result[id]['result']
      
      
    def fail(failure):
      shared_result[id]['result']=failure
      LOG.error( "WAMP FAILURE: %s", str(failure))
      e.set()
      return shared_result[id]['result']
    
    
    d = session.wamp_session.call(wamp_session_caller, kwarg['wamp_rpc_call'],*kwarg['data'])
    d.addCallback(success)	      
    d.addErrback(fail)


# OSLO ENDPOINT
class WampEndpoint(object):
    
    def __init__(self,wamp_session):
        self.wamp_session=wamp_session

    def s4t_invoke_wamp(self, ctx, **kwarg):
        e = threading.Event()
	LOG.debug( "CONDUCTOR sent me:",kwarg)

	th = threading.Thread(target=wamp_request,args=(e, kwarg,self))
	th.start()
        
        e.wait()
	LOG.debug("result received from wamp call: %s", str(shared_result[th.ident]['result']))
	
	result=shared_result[th.ident]['result']
	del shared_result[th.ident]['result']
	return result


class MyFrontendComponent(wamp.ApplicationSession):
    
    def onJoin(self, details):
        global wamp_session_caller
        wamp_session_caller=self
	LOG.info("WAMP session ready.")


    def onDisconnect(self):
	LOG.info("disconnected")
        reactor.stop()


class MyClientFactory(websocket.WampWebSocketClientFactory, ReconnectingClientFactory):
    maxDelay = 30

    def clientConnectionFailed(self, connector, reason):
        #print "reason:", reason
        LOG.warning("Wamp Connection Failed.")
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        #print "reason:", reason
        LOG.warning("Wamp Connection Lost.")
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

class RPCServer(Thread):
    def __init__(self):
        
        # AMQP CONFIG
        endpoints = [
            WampEndpoint(MyFrontendComponent),
        ]  
        
        Thread.__init__(self)
        transport_url = 'rabbit://openstack:0penstack@192.168.17.1:5672/'
        transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
        target = oslo_messaging.Target(topic='s4t_invoke_wamp', server='server1')     

        self.server = oslo_messaging.get_rpc_server(transport, target, endpoints, executor='threading')
    
    def run(self):
        
        try:
            LOG.info("Starting AMQP server... ")
            self.server.start()
            #self.server.wait()
        except KeyboardInterrupt:
            
            LOG.info("Stopping AMQP server... ")
            self.server.stop()
            LOG.info("AMQP server stopped. ")
        
            
class WampManager(object):
    def __init__(self):
      component_config = types.ComponentConfig(realm = u"s4t")
      session_factory = wamp.ApplicationSessionFactory(config = component_config)
      session_factory.session = MyFrontendComponent

      transport_factory = MyClientFactory(session_factory)
      
      transport_factory.host = '192.168.17.1'
      transport_factory.port = 8181
      websocket.connectWS(transport_factory) 
    
    def start(self):
        LOG.info("Starting WAMP server...")
        reactor.run()
        
    def stop(self):        
        LOG.info("Stopping WAMP-agent server...")
        reactor.stop()
        LOG.info("WAMP server stopped.")
