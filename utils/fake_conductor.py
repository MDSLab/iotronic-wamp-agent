#! /usr/bin/python
from oslo_config import cfg
import oslo_messaging
import sys

   
client_name = sys.argv[1] if len(sys.argv) >= 2 else 'TESTER'

uuid_agent='agent'
uuid_board='board'

s4t_topic='s4t_invoke_wamp'
full_topic=uuid_agent+'.'+s4t_topic

transport_url = 'rabbit://openstack:0penstack@controller:5672'
transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
target = oslo_messaging.Target(topic=full_topic)

client = oslo_messaging.RPCClient(transport, target)
client = client.prepare(timeout=10)


ctxt={}

def execute(uuid_agent,uuid_board,rpc_name,ctxt={},rpc_args=None):
    full_topic=uuid_agent+'.'+s4t_topic
    wamp_rpc_call=uuid_board+"."+rpc_name
    try:
        return client.call(ctxt, full_topic, wamp_rpc_call=wamp_rpc_call, data=rpc_args) 
    except Exception as e :
        return e


print execute(uuid_agent,uuid_board,'add',ctxt,( 2, 3 ))
print execute(uuid_agent,uuid_board,'hello',ctxt,(client_name, "Y O L O"))


#print execute(uuid_agent,uuid_board,'plug_and_play',ctxt,('test', 'Test'))
#print 'injected'
#print execute(uuid_agent,uuid_board,'test_function',ctxt,())
#print 'done'









