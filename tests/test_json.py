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
from lycan.message import OpenC2Command, OpenC2Response
from lycan.serializations import OpenC2MessageEncoder,OpenC2MessageDecoder

class TestJson(unittest.TestCase):
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
                   'type' : 'openc2:ipv4-addr',
                   'value': '1.2.3.4'
               },
               'actuator': {
                   'type' : 'openc2:firewall',
                   'where': 'perimeter',
               },
               'modifiers': {
                   'foo': 'bar'
               }
        }
        cmd = OpenC2Command(action=openc2.LOCATE, target=openc2.IPV4_ADDR, actuator='firewall')
        cmd.target.value = '1.2.3.4'
        cmd.actuator.where = 'perimeter'
        cmd.modifiers.foo = 'bar'
        msg = OpenC2MessageEncoder().encode(cmd)
        self.assertEqual(msg, OpenC2MessageEncoder().encode(_msg))
    def test_command_decode(self):
        _msg = {
               'action':'deny',
					'target': {
                   'type' : 'ipv4-addr',
                   'value': '1.2.3.4'
               },
               'actuator': {
                   'type': 'firewall'
               },
               'modifiers': {
                   'foo': 'bar'
               }
        }
        cmd = OpenC2MessageDecoder().decode(json.dumps(_msg))
        self.assertEqual(cmd.action, 'deny')
    def test_command_decode_invalid(self):
        _msg = {
               'action':'deny',
        }
        cmd = OpenC2MessageDecoder()
        self.assertRaises(ValueError, cmd.decode, json.dumps(_msg))
    def test_response_encode(self):
        _msg = {
               'response': {
                   'source': {
                       'type': 'firewall'
                   }
               },
               'status':'200',
               'results':'passed',
               'cmdref':1,
               'status_text':'foo'
        }
        x = OpenC2Response('firewall', '200', 'passed', 1, 'foo')
        msg = OpenC2MessageEncoder().encode(x)
        self.assertEqual(msg, OpenC2MessageEncoder().encode(_msg))
    def test_response_decode(self):
        _msg = {
               'response': {
                   'source': {
                       'type': 'firewall'
                   }
               },
               'status':'200',
               'results':'passed',
               'cmdref':1,
               'status_text':'foo'
        }
        response = OpenC2MessageDecoder().decode(json.dumps(_msg))
        self.assertEqual(response.source['type'], 'firewall')
    def test_response_decode_invalid(self):
        _msg = {
               'response': {
                   'source': {
                       'type': 'firewall'
                   }
               },
               'results':'passed',
               'cmdref':1,
               'status_text':'foo'
        }
        cmd = OpenC2MessageDecoder()
        self.assertRaises(ValueError, cmd.decode, json.dumps(_msg))
        _msg = {
               'response': {
                   'source': {
                       'type': 'firewall'
                   }
               },
               'status':'200',
               'cmdref':1,
               'status_text':'foo',
        }
        cmd = OpenC2MessageDecoder()
        self.assertRaises(ValueError, cmd.decode, json.dumps(_msg))
        _msg = {
               'response': {
               },
               'status':'200',
               'cmdref':1,
               'status_text':'foo',
        }
        cmd = OpenC2MessageDecoder()
        self.assertRaises(ValueError, cmd.decode, json.dumps(_msg))
