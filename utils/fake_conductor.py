from oslo_config import cfg
import oslo_messaging
import sys
import json


print 'Argument List:', str(sys.argv)
    
client_name = sys.argv[1] if len(sys.argv) >= 2 else '...this is a test...'
    
print 'client_name:', client_name	      


uuid_agent='agent'
s4t_topic='s4t_invoke_wamp'

transport_url = 'rabbit://openstack:0penstack@controller:5672'
transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
target = oslo_messaging.Target(topic=uuid_agent+'.'+s4t_topic)

client = oslo_messaging.RPCClient(transport, target)

ctxt={}
'''
wamp_rpc_call="com.myapp.add"
args = ( 2, 3 )
#print "DATA:",wamp_rpc_call,args
print client.call(ctxt, s4t_topic, wamp_rpc_call=wamp_rpc_call, data=args) 
'''
wamp_rpc_call="com.myapp.hello"
args = (client_name, "yolo")
#print "DATA:",wamp_rpc_call,args
print client.call(ctxt, uuid_agent+'.'+s4t_topic, wamp_rpc_call=wamp_rpc_call, data=args) 














