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
.. module: openc2.v10.message
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

import openc2

from collections import OrderedDict


class Command(openc2.base._OpenC2Base):
    _type = "command"
    _properties = OrderedDict(
        [
            (
                "action",
                openc2.properties.EnumProperty(
                    allowed=[
                        "scan",
                        "locate",
                        "query",
                        "deny",
                        "contain",
                        "allow",
                        "start",
                        "stop",
                        "restart",
                        "cancel",
                        "set",
                        "update",
                        "redirect",
                        "create",
                        "delete",
                        "detonate",
                        "restore",
                        "copy",
                        "investigate",
                        "remediate",
                    ],
                    required=True,
                ),
            ),
            ("target", openc2.properties.TargetProperty(required=True)),
            ("args", openc2.properties.ArgsProperty()),
            ("actuator", openc2.properties.ActuatorProperty()),
            ("command_id", openc2.properties.StringProperty()),
        ]
    )


class Response(openc2.base._OpenC2Base):
    _type = "response"
    _properties = OrderedDict(
        [
            ("status", openc2.properties.IntegerProperty(required=True)),
            ("status_text", openc2.properties.StringProperty()),
            ("results", openc2.properties.DictionaryProperty()),
        ]
    )
