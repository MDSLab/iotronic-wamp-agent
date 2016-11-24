from oslo_config import cfg
import oslo_messaging
import threading



# OSLO ENDPOINT for target=test
class WampEndpoint(object):
    
    def __init__(self,qin,qout):
        self.q_forwards=qin
        self.q_backwards=qout
    
    def s4t_invoke_wamp(self, ctx, arg):

        print "CONDUCTOR sent me: "+str(arg)
        
        self.q_forwards.put(arg)
        
        while self.q_backwards.empty():
            pass
        
        response = self.q_backwards.get()
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


class RPCServer(object):
    def __init__(self,qin,qout):
        
        endpoints = [
            WampEndpoint(qin,qout),
        ]  
        
        transport_url = 'rabbit://openstack:0penstack@192.168.17.1:5672/'
        transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
        target = oslo_messaging.Target(topic='s4t_invoke_wamp', server='server1')     
        
        server = oslo_messaging.get_rpc_server(transport, target, endpoints, executor='blocking')
        
        th = threading.Thread(target=oslo_rpc,args=(server,))
        th.start()
        