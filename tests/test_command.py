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

import unittest
from lycan.message import AttributeDict, OpenC2CommandField, OpenC2Command

class TestAttributeDict(unittest.TestCase):
    def setUp(self):
        self.x = AttributeDict({"foo":"bar"})
    def tearDown(self):
        pass
    def test_get_found(self):
        self.assertEqual(self.x.foo, "bar")
    def test_get_notfound(self):
        self.assertEqual(self.x.bar, None)
    def test_del(self):
        self.x.y = 1
        self.assertEqual(self.x.y, 1)
        del self.x.y
        self.assertEqual(self.x.y, None)

class TestOpenC2CommandField(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_init_str(self):
        x = OpenC2CommandField('foo')
        self.assertEqual(x, 'openc2:foo')
    def test_init_dict(self):
        x = OpenC2CommandField({'type':'foo'})
        self.assertEqual(x, 'foo')
    def test_init_notype(self):
        self.assertRaises(ValueError, OpenC2CommandField, {'foo':'bar'})
    def test_init_empty(self):
        self.assertRaises(TypeError, OpenC2CommandField, )
    def test_init_other(self):
        self.assertRaises(TypeError, OpenC2CommandField, None)
    def test_init_datamodel(self):
        x = OpenC2CommandField('foo:bar')
        self.assertNotEqual(x, 'openc2:bar')
    def test_specifier_set(self):
        x = OpenC2CommandField('foo')
        x.value = 1
        self.assertEqual(x.value, 1)
    def test_specifiers_get(self):
        x = OpenC2CommandField({'type':'foo','value':1,'y':'bar'})
        self.assertEqual(x.specifiers, {'value':1, 'y':'bar'})

class TestOpenC2Command(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_init_fail(self):
        self.assertRaises(TypeError, OpenC2Command, 'deny')
    def test_init_noactuator(self):
        x = OpenC2Command('deny','ipv4_addr')
        self.assertEqual(x.action, 'deny')
    def test_init_actuator(self):
        x = OpenC2Command('deny','ipv4_addr','firewall')
        self.assertEqual(x.actuator, 'firewall')
    def test_init_modifiers(self):
        x = OpenC2Command('deny','ipv4_addr','firewall',{'foo':'bar'})
        self.assertEqual(x.modifiers.foo, 'bar')
