from oslo_config import cfg
import oslo_messaging
import sys
import json


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


s4t_topic='s4t_invoke_wamp'

transport_url = 'rabbit://openstack:0penstack@192.168.17.1:5672'
transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
target = oslo_messaging.Target(topic=s4t_topic)

client = oslo_messaging.RPCClient(transport, target)

ctxt={}

wamp_rpc_call="com.myapp.hello"
args=[ client_name, "yolo" ]


message = {}
message['wamp_rpc_call'] = wamp_rpc_call
message['args'] = args
json_message = json.dumps(message) #{"wamp_rpc_call":"'+wamp_rpc_call+'", "args":'+args+' }


print 'message to send:', str(json_message)


print client.call(ctxt, s4t_topic, arg=json_message) 
