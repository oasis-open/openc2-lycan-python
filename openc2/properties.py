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
.. module: openc2.properties
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from stix2 import properties
from stix2.properties import Property, DictionaryProperty
from stix2.utils import _get_dict
from .base import _OpenC2Base
from .core import parse_component, parse_args
from .v10.common import Payload
from collections import OrderedDict
import re, inspect

class PayloadProperty(Property):
    def clean(self, value):
        try:
            obj = Payload(**value)
        except Exception as e:
            raise e
        return obj

class ProcessProperty(Property):
    pass

class FileProperty(Property):
    pass

#openc2 1.0 spec only supports md5, sha1, sha256
HASHES_REGEX = {
    "md5": (r"^[A-F0-9]{32}$", "md5"),
    "sha1": (r"^[A-F0-9]{40}$", "sha1"),
    "sha256": (r"^[A-F0-9]{64}$", "sha256"),
}

class HashesProperty(DictionaryProperty):
    def clean(self, value):
        clean_dict = super(HashesProperty, self).clean(value)
        for k, v in clean_dict.items():
            if k in HASHES_REGEX:
                vocab_key = HASHES_REGEX[k][1]
                if not re.match(HASHES_REGEX[k][0], v):
                    raise ValueError("'{0}' is not a valid {1} hash".format(v, vocab_key))
                if k != vocab_key:
                    clean_dict[vocab_key] = clean_dict[k]
                    del clean_dict[k]
            else:
                raise ValueError("'{1}' is not a valid hash".format(v, k))
        return clean_dict

class ComponentProperty(Property):
    def __init__(self, allow_custom=False, *args, **kwargs):
        super(ComponentProperty, self).__init__(*args, **kwargs)
        self.allow_custom = allow_custom
        self._component_type = None

    def clean(self, value):
        if not self._component_type:
            raise ValueError("This property requires a component type")
        dictified = {}
        try:
            if isinstance(value, _OpenC2Base):
                dictified[value._type]= _get_dict(value)
            else:
                dictified = _get_dict(value)
        except ValueError:
            raise ValueError("This property may only contain a dictionary or object")
        parsed_obj = parse_component(dictified, allow_custom=self.allow_custom, component_type=self._component_type)
        return parsed_obj

class TargetProperty(ComponentProperty):
    def __init__(self, allow_custom=False, *args, **kwargs):
        super(TargetProperty, self).__init__(allow_custom, *args, **kwargs)
        self.allow_custom = allow_custom
        self._component_type = "targets"

class ActuatorProperty(ComponentProperty):
    def __init__(self, allow_custom=False, *args, **kwargs):
        super(ActuatorProperty, self).__init__(allow_custom, *args, **kwargs)
        self.allow_custom = allow_custom
        self._component_type = "actuators"

class ArgsProperty(DictionaryProperty):
    def __init__(self, allow_custom=True, *args, **kwargs):
        super(ArgsProperty, self).__init__(allow_custom, *args, **kwargs)
        self.allow_custom = allow_custom

    def clean(self, value):
        dictified = {}
        try:
            dictified = _get_dict(value)
        except ValueError:
            raise ValueError("This property may only contain a dictionary or object")
        parsed_obj = parse_args(dictified, allow_custom=self.allow_custom)
        return parsed_obj
