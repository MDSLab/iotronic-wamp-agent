from oslo_config import cfg
import oslo_messaging
import sys


'''
class TestClient(object):

    def __init__(self, transport):
        target = messaging.Target(topic='test')
        self._client = messaging.RPCClient(transport, target)

    def test(self, ctxt, arg):
        return self._client.call(ctxt, 'test', arg=arg)
'''

print 'Argument List:', str(sys.argv)
    
    
client_name = str(sys.argv[1]) 
print 'client_name:', client_name	      



transport_url = 'rabbit://openstack:0penstack!@controller:5672/'
transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
target = oslo_messaging.Target(topic='test')

client = oslo_messaging.RPCClient(transport, target)

ctxt={}
message="yolo"
print 'message to send:', message
arg=[ client_name, message ]

print client.call(ctxt, 'test', arg=arg) 
