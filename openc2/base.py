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
.. module: openc2.base
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

import copy
import json
from . import exceptions
import datetime

from collections.abc import Mapping


class OpenC2JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, _OpenC2Base):
            tmp_obj = dict(copy.deepcopy(obj))
            if isinstance(obj, (_Target, _Actuator)):
                # collapse targets with a single specifier (ie, DomainName)
                if len(obj._properties) == 1 and obj._type in obj._properties.keys():
                    tmp_obj = tmp_obj.get(obj._type)
                # handle custom target specifiers
                if ":" in obj._type:
                    nsid, _type = obj._type.split(":")
                    tmp_obj = tmp_obj.get(_type)
                # for target/actuators, return type and specifiers dict
                return {obj._type: tmp_obj}
            else:
                return tmp_obj
        else:
            try:
                # support stix2 objects even tho stix2 isn't a dependency
                from stix2.base import STIXJSONEncoder

                return STIXJSONEncoder.default(self, obj)
            except:
                pass

            return super(OpenC2JSONEncoder, self).default(obj)


def get_required_properties(properties):
    return (k for k, v in properties.items() if v.required)


class _OpenC2Base(Mapping):
    def object_properties(self):
        props = set(self._properties.keys())
        custom_props = list(set(self._inner.keys()) - props)
        custom_props.sort()

        all_properties = list(self._properties.keys())
        all_properties.extend(custom_props)  # Any custom properties to the bottom

        return all_properties

    def _check_property(self, prop_name, prop, kwargs):
        if prop_name not in kwargs:
            if hasattr(prop, "default"):
                value = prop.default()
                kwargs[prop_name] = value

        if prop_name in kwargs:
            try:
                kwargs[prop_name] = prop.clean(kwargs[prop_name])
            except exceptions.InvalidValueError:
                # No point in wrapping InvalidValueError in another
                # InvalidValueError... so let those propagate.
                raise
            except Exception as exc:
                raise exceptions.InvalidValueError(
                    self.__class__, prop_name, str(exc)
                ) from exc

    def check_mutually_exclusive_properties(
        self, list_of_properties, at_least_one=True
    ):
        current_properties = self.properties_populated()
        count = len(set(list_of_properties).intersection(current_properties))
        # at_least_one allows for xor to be checked
        if count > 1 or (at_least_one and count == 0):
            raise exceptions.MutuallyExclusivePropertiesError(
                self.__class__, list_of_properties
            )

    def check_at_least_one_property(self, list_of_properties=None):
        if not list_of_properties:
            list_of_properties = sorted(list(self.__class__._properties.keys()))

        current_properties = self.properties_populated()
        list_of_properties_populated = set(list_of_properties).intersection(
            current_properties
        )

        if list_of_properties and (
            not list_of_properties_populated
            or list_of_properties_populated == set(["extensions"])
        ):
            raise exceptions.AtLeastOnePropertyError(self.__class__, list_of_properties)

    # this isn't used, but may be used in the future
    # def check_properties_dependency(
    #     self, list_of_properties, list_of_dependent_properties
    # ):
    #     failed_dependency_pairs = []
    #     for p in list_of_properties:
    #         for dp in list_of_dependent_properties:
    #             if not self.get(p) and self.get(dp):
    #                 failed_dependency_pairs.append((p, dp))
    #     if failed_dependency_pairs:
    #         raise exceptions.DependentPropertiesError(
    #             self.__class__, failed_dependency_pairs
    #         )

    def check_object_constraints(self):
        """
        Meant to be overriden by subclasses. This is called after instance creation
        """
        pass

    def __init__(self, allow_custom=False, **kwargs):
        cls = self.__class__
        self._allow_custom = allow_custom

        # Detect any keyword arguments not allowed for a specific type
        if not self._allow_custom:
            extra_kwargs = list(set(kwargs) - set(self._properties))
            if extra_kwargs:
                raise exceptions.ExtraPropertiesError(cls, extra_kwargs)

        # Remove any keyword arguments whose value is None or [] (i.e. empty list)
        setting_kwargs = {}
        props = kwargs.copy()
        for prop_name, prop_value in props.items():
            if prop_value is not None and prop_value != []:
                setting_kwargs[prop_name] = prop_value

        # Detect any missing required properties
        required_properties = set(get_required_properties(self._properties))
        missing_kwargs = required_properties - set(setting_kwargs)
        if missing_kwargs:
            raise exceptions.MissingPropertiesError(cls, missing_kwargs)

        for prop_name, prop_metadata in self._properties.items():
            self._check_property(prop_name, prop_metadata, setting_kwargs)

        # Cache defaulted optional properties for serialization
        defaulted = []
        for name, prop in self._properties.items():
            try:
                if (
                    not prop.required
                    and not hasattr(prop, "_fixed_value")
                    and prop.default() == setting_kwargs[name]
                ):
                    defaulted.append(name)
            except (AttributeError, KeyError):
                continue
        self._defaulted_optional_properties = defaulted

        self._inner = setting_kwargs

        self.check_object_constraints()

    def serialize(self, pretty=False, **kwargs):
        if pretty:
            kwargs.update({"indent": 4, "separators": (",", ": ")})
        return json.dumps(self, cls=OpenC2JSONEncoder, **kwargs)

    def __iter__(self):
        return iter(self._inner)

    def __len__(self):
        return len(self._inner)

    # OpenC2 doesnt have 'type' properties in commands - or it can't now
    def __getattr__(self, name):
        # Pickle-proofing: pickle invokes this on uninitialized instances (i.e.
        # __init__ has not run).  So no "self" attributes are set yet.  The
        # usual behavior of this method reads an __init__-assigned attribute,
        # which would cause infinite recursion.  So this check disables all
        # attribute reads until the instance has been properly initialized.
        # See https://github.com/oasis-open/cti-python-stix2/blob/master/stix2/base.py#L209
        if name == "type":
            return self._type

        unpickling = "_inner" not in self.__dict__
        if not unpickling and name in self:
            return self.__getitem__(name)
        raise AttributeError(
            "'%s' object has no attribute '%s'" % (self.__class__.__name__, name)
        )

    def __setattr__(self, name, value):
        if name == "type":
            raise exceptions.ImmutableError(self.__class__, name)
        super(_OpenC2Base, self).__setattr__(name, value)

    def __getitem__(self, key):
        if key == "type":
            return self._type

        return self._inner[key]

    def __str__(self):
        return self.serialize(pretty=True)

    def __repr__(self):
        props = [(k, self[k]) for k in self.object_properties() if self.get(k)]
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(["{0!s}={1!r}".format(k, v) for k, v in props]),
        )

    def __deepcopy__(self, memo):
        # Assume: we can ignore the memo argument, because no object will ever contain the same sub-object multiple times.
        new_inner = copy.deepcopy(self._inner, memo)
        cls = type(self)
        new_inner["allow_custom"] = self._allow_custom
        return cls(**new_inner)

    def properties_populated(self):
        return list(self._inner.keys())

    def clone(self, **kwargs):
        """
        Clone and object and assign new values
        """
        unchangable_properties = []

        try:
            new_obj_inner = copy.deepcopy(self._inner)
        except AttributeError:
            new_obj_inner = copy.deepcopy(self)
        properties_to_change = kwargs.keys()

        # XXX: Make sure certain properties aren't trying to change
        for prop in ["type", "_type"]:
            if prop in properties_to_change:
                unchangable_properties.append(prop)
        if unchangable_properties:
            raise exceptions.UnmodifiablePropertyError(unchangable_properties)

        if "allow_custom" not in kwargs:
            kwargs["allow_custom"] = self._allow_custom

        cls = type(self)

        new_obj_inner.update(kwargs)
        # Exclude properties with a value of 'None' in case data is not an instance of a _OpenC2Base subclass
        return cls(**{k: v for k, v in new_obj_inner.items() if v is not None})


class _OpenC2DataType(_OpenC2Base):
    pass


class _Target(_OpenC2Base):
    pass


class _Actuator(_OpenC2Base):
    pass
