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
.. module: openc2.custom
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from collections import OrderedDict
from .base import _OpenC2Base, _Target, _Actuator
from .core import OPENC2_OBJ_MAPS, _register_extension
from . import exceptions
from . import properties as openc2_properties


def _cls_init(cls, obj, kwargs):
    if getattr(cls, "__init__", object.__init__) is not object.__init__:
        cls.__init__(obj, **kwargs)


def _check_custom_properties(cls, properties):
    if "type" in properties.keys():
        raise exceptions.PropertyPresenceError("'type' is reserved", cls)


def _custom_target_builder(cls, type, properties, version):
    class _CustomTarget(cls, _Target):

        try:
            nsid, target = type.split(":")
        except ValueError:
            raise ValueError(
                "Invalid Extended Target name '%s': must be namespace:target format"
                % type
            )

        if len(nsid) > 16:
            raise ValueError(
                "Invalid namespace '%s': must be less than 16 characters" % type
            )

        if not properties or not isinstance(properties, list):
            raise ValueError(
                "Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]"
            )

        _type = type
        _properties = OrderedDict(properties)

        _check_custom_properties(cls, _properties)

        def __init__(self, **kwargs):
            _Target.__init__(self, **kwargs)
            _cls_init(cls, self, kwargs)

    _register_extension(_CustomTarget, object_type="targets", version=version)
    return _CustomTarget


def _custom_actuator_builder(cls, type, properties, version):
    class _CustomActuator(cls, _Actuator):

        if not type.startswith("x-"):
            raise ValueError(
                "Invalid Extended Actuator name '%s': must start with x-" % type
            )

        if not properties or not isinstance(properties, list):
            raise ValueError(
                "Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]"
            )

        _type = type
        _properties = OrderedDict(properties)

        _check_custom_properties(cls, _properties)

        def __init__(self, **kwargs):
            _Actuator.__init__(self, **kwargs)
            _cls_init(cls, self, kwargs)

    _register_extension(_CustomActuator, object_type="actuators", version=version)
    return _CustomActuator


def _custom_args_builder(cls, type, properties, version):
    class _CustomArgs(cls, _OpenC2Base):

        if not properties or not isinstance(properties, list):
            raise ValueError(
                "Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]"
            )

        _type = type
        _properties = OrderedDict(properties)

        _check_custom_properties(cls, _properties)

        def __init__(self, **kwargs):
            _OpenC2Base.__init__(self, **kwargs)
            _cls_init(cls, self, kwargs)

    _register_extension(_CustomArgs, object_type="args", version=version)
    return _CustomArgs


def _custom_property_builder(cls, type, properties, version):
    class _CustomProperty(cls, _OpenC2Base, openc2_properties.Property):

        if not properties or not isinstance(properties, list):
            raise ValueError(
                "Must supply a list, containing tuples. For example, [('property1', IntegerProperty())]"
            )

        _type = type
        _properties = OrderedDict(properties)

        _check_custom_properties(cls, _properties)

        def __init__(
            self, required=False, fixed=None, default=None, allow_custom=False, **kwargs
        ):

            _OpenC2Base.__init__(self, allow_custom=allow_custom, **kwargs)
            _cls_init(cls, self, kwargs)
            openc2_properties.Property.__init__(
                self, required=required, fixed=fixed, default=default
            )

            if kwargs:
                self.clean(self)

        def __call__(self, _value=None, **kwargs):
            """__init__ for when using an instance
            Example: Used by ListProperty to handle lists that have been defined with
            either a class or an instance.
            """
            if _value:
                return _value

            value = self.__class__(**kwargs)
            return self.clean(value)

    _register_extension(_CustomProperty, object_type="properties", version=version)
    return _CustomProperty
