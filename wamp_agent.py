#!/usr/bin/env python

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Iotronic Wamp Agent
"""


from iotronic.wamp.agent import WampAgent
from oslo_config import cfg


wamp_opts = [
    cfg.StrOpt('wamp_transport_url',
            default='ws://192.168.17.1:8181/',
            help=('URL of wamp broker')),
    cfg.StrOpt('wamp_realm',
            default='s4t',
            help=('realm broker')),
]


CONF = cfg.CONF
CONF.register_opts(wamp_opts, 'wamp')

###################
CONF.debug=True
CONF.transport_url='rabbit://openstack:0penstack@controller:5672/'
###################

if __name__ == '__main__':
    wa=WampAgent(CONF)