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
.. module: openc2.v10.targets
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from stix2 import properties
from ..properties import PayloadProperty, HashesProperty, ProcessProperty, FileProperty
from ..base import _Target, OpenC2JSONEncoder
from ..custom import _custom_target_builder

import itertools
import copy
from collections import OrderedDict

class Artifact(_Target):
    _type = 'artifact'
    _properties = OrderedDict([
        ('mime_type', properties.StringProperty()),
        ('payload', PayloadProperty()),
        ('hashes', HashesProperty()),
    ])

    def _check_object_constraints(self):
        super(Artifact, self)._check_object_constraints()
        self._check_at_least_one_property()

class Device(_Target):
    _type = 'device'
    _properties = OrderedDict([
        ('hostname', properties.StringProperty()),
        ('idn_hostname', properties.StringProperty()),
        ('device_id', properties.StringProperty())
    ])

class DomainName(_Target):
    _type = 'domain_name'
    _properties = OrderedDict([
        ('domain_name', properties.StringProperty(required=True)),
    ])

class EmailAddress(_Target):
    _type = 'email_addr'
    _properties = OrderedDict([
        ('email_addr', properties.StringProperty(required=True)),
    ])

class Features(_Target): 
    _type = 'features'
    _properties = OrderedDict([
        ('features', properties.ListProperty(properties.StringProperty))
    ])

    def _check_object_constraints(self):
        super(Features, self)._check_object_constraints()
        self._check_at_least_one_property()
        if 'features' in self._inner:
            features = self._inner['features']
            if len(features) > 10:
                raise ValueError("Maximum of 10 features allowed")
            for feature in features:
                if feature not in ["versions", "profiles", "pairs", "rate_limit"]:
                    raise ValueError("%s unsupported feature")

class File(_Target): 
    _type = 'file'
    _properties = OrderedDict([
        ('name', properties.StringProperty()),
        ('path', properties.StringProperty()),
        ('hashes', HashesProperty())
    ])

    def _check_object_constraints(self):
        super(File, self)._check_object_constraints()
        self._check_at_least_one_property()

class InternationalizedDomainName(_Target):
    _type = 'idn_domain_name'
    _properties = OrderedDict([
        ('idn_domain_name', properties.StringProperty(required=True)),
    ])

class InternationalizedEmailAddress(_Target):
    _type = 'idn_email_addr'
    _properties = OrderedDict([
        ('idn_email_addr', properties.StringProperty(required=True)),
    ])

class IPv4Address(_Target):
    _type = 'ipv4_net'
    _properties = OrderedDict([
        ('ipv4_net', properties.StringProperty(required=True)),
    ])

class IPv6Address(_Target):
    _type = 'ipv6_net'
    _properties = OrderedDict([
        ('ipv6_net', properties.StringProperty(required=True)),
    ])

class IPv4Connection(_Target):
    _type = 'ipv4_connection'
    _properties = OrderedDict([
        ('src_addr', properties.StringProperty()),
        ('src_port', properties.IntegerProperty(min=0, max=65535)),
        ('dst_addr', properties.StringProperty()),
        ('dst_port', properties.IntegerProperty(min=0, max=65535)),
        ('protocol', properties.EnumProperty(
            allowed=[
                "icmp",
                "tcp",
                "udp",
                "sctp"
            ]
        ))
    ])

    def _check_object_constraints(self):
        super(IPv4Connection, self)._check_object_constraints()
        self._check_at_least_one_property()

class IPv6Connection(_Target):
    _type = 'ipv6_connection'
    _properties = OrderedDict([
        ('src_addr', properties.StringProperty()),
        ('src_port', properties.IntegerProperty(min=0, max=65535)),
        ('dst_addr', properties.StringProperty()),
        ('dst_port', properties.IntegerProperty(min=0, max=65535)),
        ('protocol', properties.EnumProperty(
            allowed=[
                "icmp",
                "tcp",
                "udp",
                "sctp"
            ]
        ))
    ])

    def _check_object_constraints(self):
        super(IPv6Connection, self)._check_object_constraints()
        self._check_at_least_one_property()

class IRI(_Target):
    _type = 'iri'
    _properties = OrderedDict([
        ('iri', properties.StringProperty(required=True)),
    ])

class MACAddress(_Target):
    _type = 'mac_addr'
    _properties = OrderedDict([
        ('mac_addr', properties.StringProperty(required=True)),
    ])

class Process(_Target):
    _type = 'process'
    _properties = OrderedDict([
        ('pid', properties.IntegerProperty()),
        ('name', properties.StringProperty()),
        ('cwd', properties.StringProperty()),
        ('executable', FileProperty()),
        ('parent', ProcessProperty()),
        ('command_line', properties.StringProperty()),
    ])

    def __init__(self, allow_custom=False, **kwargs):
        super(Process, self).__init__(allow_custom, **kwargs)

    def _check_object_constraints(self):
        super(Process, self)._check_object_constraints()
        self._check_at_least_one_property()
        if self.get('parent'):
            dictified = dict(self.get('parent'))
            try:
                Process(**dictified)
            except Exception as e:
                raise e
            self._inner['parent'] = dictified
        if self.get('executable'):
            dictified = dict(self.get('executable'))
            try:
                File(**dictified)
            except Exception as e:
                raise e
            self._inner['executable'] = dictified

class Properties(_Target):
    _type = 'properties'
    _properties = OrderedDict([
        ('properties', properties.ListProperty(properties.StringProperty)),
    ])

class URI(_Target):
    _type = 'uri'
    _properties = OrderedDict([
        ('uri', properties.StringProperty(required=True)),
    ])

def CustomTarget(type='x-acme', properties=None):
    def wrapper(cls):
        _properties = list(itertools.chain.from_iterable([
            [x for x in properties if not x[0].startswith('x_')],
            sorted([x for x in properties if x[0].startswith('x_')], key=lambda x: x[0]),
        ]))
        return _custom_target_builder(cls, type, _properties, '2.1')

    return wrapper
