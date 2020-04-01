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
import openc2

import itertools
from collections import OrderedDict


class SLPFActuator(openc2.base._Actuator):
    _type = "slpf"
    _properties = OrderedDict(
        [
            ("hostname", openc2.properties.StringProperty()),
            ("named_group", openc2.properties.StringProperty()),
            ("asset_id", openc2.properties.StringProperty()),
            (
                "asset_tuple",
                openc2.properties.ListProperty(openc2.properties.StringProperty),
            ),
        ]
    )

    def check_object_constraints(self):
        super(SLPFActuator, self).check_object_constraints()

        if "asset_tuple" in self:
            if len(self.asset_tuple) > 10:
                raise openc2.exceptions.InvalidValueError(
                    self.__class__, "asset_tuple", "Maximum of 10 features allowed"
                )


class SLPFTarget(openc2.base._Target):
    _type = "slpf:rule_number"
    _properties = OrderedDict(
        [("rule_number", openc2.properties.StringProperty(required=True)),]
    )


class SLPFArgs(openc2.base._OpenC2Base):
    _type = "slpf"
    _properties = OrderedDict(
        [
            (
                "drop_process",
                openc2.properties.EnumProperty(
                    allowed=["none", "reject", "false_ack",]
                ),
            ),
            (
                "persistent",
                openc2.properties.EnumProperty(
                    allowed=["none", "reject", "false_ack",]
                ),
            ),
            (
                "direction",
                openc2.properties.EnumProperty(allowed=["both", "ingress", "egress",]),
            ),
            ("insert_rule", openc2.properties.IntegerProperty()),
        ]
    )


class SLPF(openc2.base._OpenC2Base):
    _type = "slpf"
    _properties = OrderedDict(
        [
            (
                "action",
                openc2.properties.EnumProperty(
                    allowed=["query", "deny", "allow", "update", "delete",],
                    required=True,
                ),
            ),
            ("target", openc2.properties.TargetProperty(required=True)),
            ("args", openc2.properties.ArgsProperty()),
            ("actuator", openc2.properties.ActuatorProperty()),
            ("command_id", openc2.properties.StringProperty()),
        ]
    )

    def check_object_constraints(self):
        super(SLPF, self).check_object_constraints()
        if not isinstance(self.target, openc2.base._Target) or not self.target.type in [
            "features",
            "file",
            "ipv4_net",
            "ipv6_net",
            "ipv4_connection",
            "ipv6_connection",
            "slpf:rule_number",
        ]:
            raise ValueError("Unsupported target (%s)" % self.target)
        if "actuator" in self and not isinstance(self.actuator, SLPFActuator):
            raise ValueError("Unsupported actuator (%s)" % self.actuator._type)
