# Iotronic Wamp Agent

WAMP wrapper for Iotronic: connection between AMQP and WAMP world!

* s4t-broker: machine where Conductor (broker) and Wamp-agent are running.

* s4t-device: machine represents the device (board, server and so on) that exposes WAMP RPCs.

Scenario:

1. Conductor sends a request via AMQP (with Openstack Oslo libraries)
2. Wamp-agent receives the Conductor request and forward it to the WAMP (client) thread via Python Queue module; then the WAMP client forwards the request to the device.
3. The Device receives the RPC WAMP request from the Wamp-agent, and executes the RPC function; at the end the RPC function returns the result to the Wamp-agent and it will forward this result to the Conductor.
