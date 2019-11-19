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

from stix2 import properties
from ..base import _OpenC2Base
from ..custom import _custom_args_builder

import itertools
from collections import OrderedDict

class Args(_OpenC2Base):
    _type = 'args'
    _properties = OrderedDict([
        ('start_time', properties.IntegerProperty()),
        ('stop_time', properties.IntegerProperty()),
        ('duration', properties.IntegerProperty()),
        ('response_requested', properties.EnumProperty(
            allowed=[
                "none",
                "ack",
                "status",
                "complete"
            ] 
        ))
    ])

def CustomArgs(type='x-acme', properties=None):
    def wrapper(cls):
        _properties = list(itertools.chain.from_iterable([
            [x for x in properties if not x[0].startswith('x_')],
            sorted([x for x in properties if x[0].startswith('x_')], key=lambda x: x[0]),
        ]))
        return _custom_args_builder(cls, type, _properties, '2.1')

    return wrapper