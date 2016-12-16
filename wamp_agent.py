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


from iotronic.wamp.agent import RPCServer
from iotronic.wamp.agent import WampManager


if __name__ == '__main__':
    r=RPCServer()
    w=WampManager()

    try:
        r.start()
        w.start()
    except KeyboardInterrupt:
        w.stop()
        r.stop()
        exit()