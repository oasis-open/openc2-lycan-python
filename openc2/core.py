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

import copy
import importlib
import pkgutil
import re
from . import exceptions

OPENC2_OBJ_MAPS = {}

from . import utils


def _register_extension(new_type, object_type, version=None):
    EXT_MAP = OPENC2_OBJ_MAPS["extensions"]
    EXT_MAP[object_type][new_type._type] = new_type


def _collect_openc2_mappings():
    if not OPENC2_OBJ_MAPS:
        top_level_module = importlib.import_module("openc2")
        path = top_level_module.__path__
        prefix = str(top_level_module.__name__) + "."

        for module_loader, name, is_pkg in pkgutil.walk_packages(
            path=path, prefix=prefix
        ):
            ver = name.split(".")[1]
            if re.match(r"openc2\.v1[0-9]$", name) and is_pkg:
                mod = importlib.import_module(name, str(top_level_module.__name__))
                OPENC2_OBJ_MAPS["objects"] = mod.OBJ_MAP
                OPENC2_OBJ_MAPS["targets"] = mod.OBJ_MAP_TARGET
                OPENC2_OBJ_MAPS["args"] = mod.OBJ_MAP_ARGS
                OPENC2_OBJ_MAPS["actuators"] = mod.OBJ_MAP_ACTUATOR
                OPENC2_OBJ_MAPS["extensions"] = mod.EXT_MAP
