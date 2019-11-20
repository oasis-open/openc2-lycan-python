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
.. module: openc2.core
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from stix2.utils import _get_dict
from stix2.exceptions import CustomContentError, ParseError

import copy
import importlib
import pkgutil
import re

OPENC2_OBJ_MAPS = {}

def parse(data, allow_custom=False, version=None):
    # convert OpenC2 object to dict, if not already
    obj = _get_dict(data)
    # convert dict to full python-openc2 obj
    obj = dict_to_openc2(obj, allow_custom, version)

    return obj

def dict_to_openc2(openc2_dict, allow_custom=False, version=None):
    message_type = None
    if 'action' in openc2_dict:
        message_type = 'command'
    elif 'status' in openc2_dict:
        message_type = 'response'
    else:
        raise ParseError("Can't parse object that is not valid command or response: %s" % str(openc2_dict))

    OBJ_MAP = OPENC2_OBJ_MAPS['objects']
    try:
        obj_class = OBJ_MAP[message_type]
    except KeyError:
        if allow_custom:
            return openc2_dict
        raise ParseError("Can't parse unknown object type '%s'! For custom types, use the CustomObject decorator." % openc2_dict['type'])

    return obj_class(allow_custom=allow_custom, **openc2_dict)

def parse_component(data, allow_custom=False, version=None, component_type=None):
    obj = _get_dict(data)
    obj = copy.deepcopy(obj)
    try:
        _type = list(obj.keys())[0]
        _specifiers = list(obj.values())[0]
    except IndexError:
        raise ParseError("Can't parse object that contains an invalid field: %s" % str(data))

    try:
        OBJ_MAP = OPENC2_OBJ_MAPS[component_type]
        obj_class = OBJ_MAP[_type]
    except KeyError:
        # check for extension
        try:
            EXT_MAP = OPENC2_OBJ_MAPS["extensions"]
            obj_class = EXT_MAP[component_type][_type]
        except KeyError:
            if allow_custom:
                return obj
            raise CustomContentError("Can't parse unknown target/actuator type '%s'!" % _type)
    if isinstance(_specifiers, dict):
        obj = obj[_type]

    return obj_class(allow_custom=allow_custom, **obj)

def parse_target(data, allow_custom=False, version=None):
    return parse_component(data, allow_custom, version, component_type="targets")

def parse_actuator(data, allow_custom=False, version=None):
    return parse_component(data, allow_custom, version, component_type="actuators")

def parse_args(data, allow_custom=False, version=None):
    dictified = copy.deepcopy(data)
    default_args = list(OPENC2_OBJ_MAPS["args"]["args"]._properties.keys())
    specific_type_map = OPENC2_OBJ_MAPS["extensions"]["args"]
    #iterate over each key and if its not in the default args, check extensions
    for key, subvalue in dictified.items():
        if key in default_args:
            continue
        #handle embedded custom args
        if key in specific_type_map:
            cls = specific_type_map[key]
            if type(subvalue) is dict:
                if allow_custom:
                    subvalue['allow_custom'] = True
                    dictified[key] = cls(**subvalue)
                else:
                    dictified[key] = cls(**subvalue)
                    print(type(dictified[key]))
            elif type(subvalue) is cls:
                # If already an instance of an _Extension class, assume it's valid
                dictified[key] = subvalue
            else:
                raise ValueError("Cannot determine extension type.")
        else:
            if allow_custom:
                dictified[key] = subvalue
            else:
                raise CustomContentError("Can't parse unknown extension type: {}".format(key))
    try:
        OBJ_MAP = OPENC2_OBJ_MAPS["args"]
        obj_class = OBJ_MAP["args"]
    except KeyError:
        raise CustomContentError("Can't parse args '%s!" % data) 

    return obj_class(allow_custom=allow_custom, **dictified)

def _register_extension(new_type, object_type, version=None):
    EXT_MAP = OPENC2_OBJ_MAPS['extensions']
    EXT_MAP[object_type][new_type._type] = new_type

def _collect_openc2_mappings():
    if not OPENC2_OBJ_MAPS:
        top_level_module = importlib.import_module('openc2')
        path = top_level_module.__path__
        prefix = str(top_level_module.__name__) + '.'

        for module_loader, name, is_pkg in pkgutil.walk_packages(path=path, prefix=prefix):
            ver = name.split('.')[1]
            if re.match(r'openc2\.v1[0-9]$', name) and is_pkg:
                mod = importlib.import_module(name, str(top_level_module.__name__))
                OPENC2_OBJ_MAPS['objects'] = mod.OBJ_MAP
                OPENC2_OBJ_MAPS['targets'] = mod.OBJ_MAP_TARGET
                OPENC2_OBJ_MAPS['args'] = mod.OBJ_MAP_ARGS
                OPENC2_OBJ_MAPS['actuators'] = mod.OBJ_MAP_ACTUATOR
                OPENC2_OBJ_MAPS['extensions'] = mod.EXT_MAP
