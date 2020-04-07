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
.. module: openc2.v10.args
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""
import openc2
from ..custom import _custom_args_builder

import itertools
from collections import OrderedDict


class Args(openc2.base._OpenC2Base):
    _type = "args"
    _properties = OrderedDict(
        [
            ("start_time", openc2.properties.DateTimeProperty()),
            ("stop_time", openc2.properties.DateTimeProperty()),
            ("duration", openc2.properties.IntegerProperty(min=0)),
            (
                "response_requested",
                openc2.properties.EnumProperty(
                    allowed=["none", "ack", "status", "complete"]
                ),
            ),
        ]
    )

    def check_object_constraints(self):
        super(Args, self).check_object_constraints()
        if "stop_time" in self and "start_time" in self and "duration" in self:
            raise openc2.exceptions.PropertyPresenceError(
                "start_time, stop_time, duration: Only two of the three are allowed on any given Command and the third is derived from the equation stop_time = start_time + duration.",
                self.__class__,
            )

        if "stop_time" in self and "start_time" in self:
            if self.stop_time < self.start_time:
                raise openc2.exceptions.InvalidValueError(
                    self.__class__,
                    "stop_time",
                    reason="stop_time must be greater than start_time",
                )


def CustomArgs(type="x-acme", properties=None):
    def wrapper(cls):
        _properties = list(
            itertools.chain.from_iterable(
                [
                    [x for x in properties if not x[0].startswith("x_")],
                    sorted(
                        [x for x in properties if x[0].startswith("x_")],
                        key=lambda x: x[0],
                    ),
                ]
            )
        )
        return _custom_args_builder(cls, type, _properties, "2.1")

    return wrapper
