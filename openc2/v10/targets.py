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


import openc2

import itertools
import copy
from collections import OrderedDict


class Artifact(openc2.base._Target):
    _type = "artifact"
    _properties = OrderedDict(
        [
            ("mime_type", openc2.properties.StringProperty()),
            ("payload", openc2.properties.PayloadProperty()),
            ("hashes", openc2.properties.HashesProperty()),
        ]
    )

    def check_object_constraints(self):
        super(Artifact, self).check_object_constraints()
        self.check_at_least_one_property()


class Device(openc2.base._Target):
    _type = "device"
    _properties = OrderedDict(
        [
            ("hostname", openc2.properties.StringProperty()),
            ("idn_hostname", openc2.properties.StringProperty()),
            ("device_id", openc2.properties.StringProperty()),
        ]
    )


class DomainName(openc2.base._Target):
    _type = "domain_name"
    _properties = OrderedDict(
        [("domain_name", openc2.properties.StringProperty(required=True)),]
    )


class EmailAddress(openc2.base._Target):
    _type = "email_addr"
    _properties = OrderedDict(
        [("email_addr", openc2.properties.StringProperty(required=True)),]
    )


class Features(openc2.base._Target):
    _type = "features"
    _properties = OrderedDict(
        [
            (
                "features",
                openc2.properties.ListProperty(
                    openc2.properties.EnumProperty(
                        allowed=["versions", "pairs", "profiles", "rate_limit"]
                    ),
                    default=lambda: [],
                ),
            )
        ]
    )

    def __init__(self, features=None, *args, **kwargs):
        # check_object_constraints wasn't called unless features was declared here
        super(Features, self).__init__(features=features, *args, **kwargs)

    def check_object_constraints(self):
        super(Features, self).check_object_constraints()

        seen = []
        for feature in self.features:
            if feature in seen:
                raise openc2.exceptions.InvalidValueError(
                    self.__class__,
                    "features",
                    "A Producer MUST NOT send a list containing more than one instance of any Feature.",
                )
            seen.append(feature)


class File(openc2.base._Target):
    _type = "file"
    _properties = OrderedDict(
        [
            ("name", openc2.properties.StringProperty()),
            ("path", openc2.properties.StringProperty()),
            ("hashes", openc2.properties.HashesProperty()),
        ]
    )

    def check_object_constraints(self):
        super(File, self).check_object_constraints()
        self.check_at_least_one_property()


class InternationalizedDomainName(openc2.base._Target):
    _type = "idn_domain_name"
    _properties = OrderedDict(
        [("idn_domain_name", openc2.properties.StringProperty(required=True)),]
    )


class InternationalizedEmailAddress(openc2.base._Target):
    _type = "idn_email_addr"
    _properties = OrderedDict(
        [("idn_email_addr", openc2.properties.StringProperty(required=True)),]
    )


class IPv4Address(openc2.base._Target):
    _type = "ipv4_net"
    _properties = OrderedDict(
        [("ipv4_net", openc2.properties.StringProperty(required=True)),]
    )


class IPv6Address(openc2.base._Target):
    _type = "ipv6_net"
    _properties = OrderedDict(
        [("ipv6_net", openc2.properties.StringProperty(required=True)),]
    )


class IPv4Connection(openc2.base._Target):
    _type = "ipv4_connection"
    _properties = OrderedDict(
        [
            ("src_addr", openc2.properties.StringProperty()),
            ("src_port", openc2.properties.IntegerProperty(min=0, max=65535)),
            ("dst_addr", openc2.properties.StringProperty()),
            ("dst_port", openc2.properties.IntegerProperty(min=0, max=65535)),
            (
                "protocol",
                openc2.properties.EnumProperty(allowed=["icmp", "tcp", "udp", "sctp"]),
            ),
        ]
    )

    def check_object_constraints(self):
        super(IPv4Connection, self).check_object_constraints()
        self.check_at_least_one_property()


class IPv6Connection(openc2.base._Target):
    _type = "ipv6_connection"
    _properties = OrderedDict(
        [
            ("src_addr", openc2.properties.StringProperty()),
            ("src_port", openc2.properties.IntegerProperty(min=0, max=65535)),
            ("dst_addr", openc2.properties.StringProperty()),
            ("dst_port", openc2.properties.IntegerProperty(min=0, max=65535)),
            (
                "protocol",
                openc2.properties.EnumProperty(allowed=["icmp", "tcp", "udp", "sctp"]),
            ),
        ]
    )

    def check_object_constraints(self):
        super(IPv6Connection, self).check_object_constraints()
        self.check_at_least_one_property()


class IRI(openc2.base._Target):
    _type = "iri"
    _properties = OrderedDict(
        [("iri", openc2.properties.StringProperty(required=True)),]
    )


class MACAddress(openc2.base._Target):
    _type = "mac_addr"
    _properties = OrderedDict(
        [("mac_addr", openc2.properties.StringProperty(required=True)),]
    )


class Process(openc2.base._Target):
    _type = "process"
    _properties = OrderedDict(
        [
            ("pid", openc2.properties.IntegerProperty()),
            ("name", openc2.properties.StringProperty()),
            ("cwd", openc2.properties.StringProperty()),
            ("executable", openc2.properties.FileProperty()),
            ("parent", openc2.properties.ProcessProperty()),
            ("command_line", openc2.properties.StringProperty()),
        ]
    )

    def __init__(self, allow_custom=False, **kwargs):
        super(Process, self).__init__(allow_custom, **kwargs)

    def check_object_constraints(self):
        super(Process, self).check_object_constraints()
        self.check_at_least_one_property()


class Properties(openc2.base._Target):
    _type = "properties"
    _properties = OrderedDict(
        [
            (
                "properties",
                openc2.properties.ListProperty(openc2.properties.StringProperty),
            ),
        ]
    )


class URI(openc2.base._Target):
    _type = "uri"
    _properties = OrderedDict(
        [("uri", openc2.properties.StringProperty(required=True)),]
    )


def CustomTarget(type="x-acme", properties=None):
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
        return openc2.custom._custom_target_builder(cls, type, _properties, "2.1")

    return wrapper
