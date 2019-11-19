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
.. module: openc2.v10
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from .message import Command, Response

from .targets import (
    Artifact, Device, DomainName, EmailAddress, Features, File,
    InternationalizedDomainName, InternationalizedEmailAddress, IPv4Address,
    IPv6Address, IPv4Connection, IPv6Connection, IRI, MACAddress, Process,
    Properties, URI, CustomTarget
)

from .common import Payload
from .args import Args, CustomArgs
from .actuators import CustomActuator
from .slpf import SLPFTarget, SLPFActuator, SLPFArgs

OBJ_MAP = {
    'command': Command,
    'response': Response
}

OBJ_MAP_TARGET = {
    'artifact': Artifact,
    'device': Device,
    'domain_name': DomainName,
    'email_addr': EmailAddress,
    'features': Features,
    'file': File,
    'idn_domain_name': InternationalizedDomainName,
    'idn_email_addr': InternationalizedEmailAddress,
    'ipv4_net': IPv4Address,
    'ipv6_net': IPv6Address,
    'ipv4_connection': IPv4Connection,
    'ipv6_connection': IPv6Connection,
    'iri': IRI,
    'mac_addr': MACAddress,
    'process': Process,
    'properties': Properties,
    'uri': URI,
    'slpf:rule_number': SLPFTarget
}

OBJ_MAP_ACTUATOR = {
    'slpf': SLPFActuator
}

OBJ_MAP_ARGS = {
    'args': Args,
}

EXT_MAP = {
    'targets': {'slpf:rule_number':SLPFTarget},
    'actuators': {'slpf': SLPFActuator},
    'args': {'slpf':SLPFArgs}
}
