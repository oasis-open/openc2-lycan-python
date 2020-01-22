#
#  The MIT License (MIT)
#
# Copyright 2019 AT&T Intellectual Property. All other rights reserved.
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

"""
.. module: openc2.v10.slpf
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from stix2 import properties
from ..base import _OpenC2Base, _Actuator, _Target
from ..properties import TargetProperty, ActuatorProperty, ArgsProperty

import itertools
from collections import OrderedDict

class SLPFActuator(_Actuator):
    _type = 'slpf'
    _properties = OrderedDict([
        ('hostname', properties.StringProperty()),
        ('named_group', properties.StringProperty()),
        ('asset_id', properties.StringProperty()),
        ('asset_tuple', properties.StringProperty()),
    ])

class SLPFTarget(_Target):
    _type = 'slpf:rule_number'
    _properties = OrderedDict([
        ('rule_number', properties.IntegerProperty(required=True)),
    ])

class SLPFArgs(_OpenC2Base):
    _type = 'slpf'
    _properties = OrderedDict([
        ('drop_process', properties.EnumProperty(
            allowed=[
                "none",
                "reject",
                "false_ack",
            ] 
        )),
        ('persistent', properties.EnumProperty(
            allowed=[
                "none",
                "reject",
                "false_ack",
            ] 
        )),
        ('direction', properties.EnumProperty(
            allowed=[
                "both",
                "ingress",
                "egress",
            ] 
        )),
        ('insert_rule', properties.IntegerProperty()),
    ])

class SLPF(_OpenC2Base):
    _type = 'slpf'
    _properties = OrderedDict([
        ('action', properties.EnumProperty(
            allowed=[
                "query",
                "deny",
                "allow",
                "update",
                "delete",
            ], required=True
        )),
        ('target', TargetProperty(required=True)),
        ('args', ArgsProperty()),
        ('actuator', ActuatorProperty()),
        ('command_id', properties.StringProperty())
    ])

    def _check_object_constraints(self):
        super(SLPF, self)._check_object_constraints()
        if not isinstance(self.target, _Target) or not self.target.type \
                in ['features', 'file', 'ipv4_net', 'ipv6_net', 'ipv4_connection', 
                        'ipv6_connection', 'slpf:rule_number']:
            raise ValueError("Unsupported target (%s)"%self.target)
        if self.actuator and not isinstance(self.actuator, SLPFActuator):
            raise ValueError("Unsupported actuator (%s)"%self.actuator._type)
