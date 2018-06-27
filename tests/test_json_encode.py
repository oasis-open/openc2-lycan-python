#
#  The MIT License (MIT)
#
# Copyright 2018 AT&T Intellectual Property. All other rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import unittest,json
import lycan.datamodels as openc2
from lycan.message import OpenC2Command, OpenC2Response, OpenC2Target, OpenC2Actuator, OpenC2Header, OpenC2Message
from lycan.serializations import OpenC2MessageEncoder

class TestJsonEncode(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_encode(self):
        _msg = {'foo':'bar'}
        msg = OpenC2MessageEncoder().encode(_msg)
        self.assertEqual(msg, json.dumps(_msg))

    def test_command_encode(self):
        _msg = {
               'action':'locate',
               'target': {
                   'ip_addr': '1.2.3.4'
               },
               'actuator': {
                   'network_firewall': {
                       'where': 'perimeter'
                   }
               },
               'args': {
                   'foo': 'bar'
               }
        }
        cmd = OpenC2Command(action=openc2.LOCATE, target=OpenC2Target(openc2.IP_ADDR, '1.2.3.4'),
                            actuator=OpenC2Actuator(openc2.NETWORK_FIREWALL))
        cmd.actuator.where = 'perimeter'
        cmd.args.foo = 'bar'
        msg = OpenC2MessageEncoder().encode(cmd)
        self.assertEqual(msg, OpenC2MessageEncoder().encode(_msg))

        _msg = {
               'action':'locate',
               'target': {
                   'file': {
                       'name': 'passwd',
                       'hashes': '0x129823'
                   }
               },
               'args': {
                   'foo': 'bar'
               }
        }
        cmd = OpenC2Command(action=openc2.LOCATE, target=OpenC2Target(openc2.FILE, name="passwd"), args={'foo':'bar'})
        cmd.target.hashes = '0x129823'
        msg = OpenC2MessageEncoder().encode(cmd)
        self.assertEqual(msg, OpenC2MessageEncoder().encode(_msg))

    def test_response_encode(self):
        _msg = {
               'id': 'test1',
               'id_ref': 'cmd1',
               'status':'200',
               'status_text':'passed',
               'results':'foo'
        }
        x = OpenC2Response('test1', 'cmd1', '200', 'passed', 'foo')
        msg = OpenC2MessageEncoder().encode(x)
        self.assertEqual(msg, OpenC2MessageEncoder().encode(_msg))

    def test_message_encode_invalid(self):
        msg = OpenC2Message(OpenC2Header())
        cmd = OpenC2MessageEncoder()
        self.assertRaises(ValueError, cmd.encode, msg)

    def test_message_encode(self):
        _msg = {
               'header': {
                   'version': '0.1.0',
                   'content_type': 'application/json'
               },
               'command': {
                   'action':'deny',
                   'target': {
                       'ip_addr': '1.2.3.4'
                   },
                   'args': {
                       'foo': 'bar'
                   }
              }
        }
        hdr = OpenC2Header()
        body = OpenC2Command(action=openc2.DENY, target=OpenC2Target(openc2.IP_ADDR, '1.2.3.4'), args={'foo':'bar'})
        msg = OpenC2Message(hdr, body)
        self.assertEqual(OpenC2MessageEncoder().encode(msg), OpenC2MessageEncoder().encode(_msg))

        _msg = {
               'header': {
                   'version': '0.1.0',
                   'id': 'resp1',
                   'created': 'now',
                   'sender': 'firewall',
                   'content_type': 'application/json'
               },
               'response': {
                   'id': 'resp1',
                   'id_ref': 'cmd1',
                   'status': 200
              }
        }
        hdr = OpenC2Header(id='resp1', created='now', sender='firewall')
        body = OpenC2Response('resp1', 'cmd1', 200)
        msg = OpenC2Message(hdr, body)
        self.assertEqual(OpenC2MessageEncoder().encode(msg), OpenC2MessageEncoder().encode(_msg))
