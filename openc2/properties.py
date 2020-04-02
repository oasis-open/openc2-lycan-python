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
import base64
import binascii
from .base import _OpenC2Base
from collections import OrderedDict
from .custom import _custom_property_builder
from . import utils
from . import exceptions
import re, inspect
import itertools
import datetime
import copy
from collections import OrderedDict
from collections.abc import Mapping


class Property(object):
    """Represent a property of STIX data type.
    Subclasses can define the following attributes as keyword arguments to
    ``__init__()``.
    Args:
        required (bool): If ``True``, the property must be provided when
            creating an object with that property. No default value exists for
            these properties. (Default: ``False``)
        fixed: This provides a constant default value. Users are free to
            provide this value explicity when constructing an object (which
            allows you to copy **all** values from an existing object to a new
            object), but if the user provides a value other than the ``fixed``
            value, it will raise an error. This is semantically equivalent to
            defining both:
            - a ``clean()`` function that checks if the value matches the fixed
              value, and
            - a ``default()`` function that returns the fixed value.
    Subclasses can also define the following functions:
    - ``def clean(self, value) -> any:``
        - Return a value that is valid for this property. If ``value`` is not
          valid for this property, this will attempt to transform it first. If
          ``value`` is not valid and no such transformation is possible, it
          should raise an exception.
    - ``def default(self):``
        - provide a default value for this property.
        - ``default()`` can return the special value ``NOW`` to use the current
            time. This is useful when several timestamps in the same object
            need to use the same default value, so calling now() for each
            property-- likely several microseconds apart-- does not work.
    Subclasses can instead provide a lambda function for ``default`` as a
    keyword argument. ``clean`` should not be provided as a lambda since
    lambdas cannot raise their own exceptions.
    When instantiating Properties, ``required`` and ``default`` should not be
    used together. ``default`` implies that the property is required in the
    specification so this function will be used to supply a value if none is
    provided. ``required`` means that the user must provide this; it is
    required in the specification and we can't or don't want to create a
    default value.
    """

    def _default_clean(self, value):
        if value != self._fixed_value:
            raise ValueError("must equal '{}'.".format(self._fixed_value))
        return value

    def __init__(self, required=False, fixed=None, default=None):
        self.required = required
        if fixed:
            self._fixed_value = fixed
            self.clean = self._default_clean
            self.default = lambda: fixed
        if default:
            self.default = default

    def clean(self, value):
        return value

    def __call__(self, value=None):
        """Used by ListProperty to handle lists that have been defined with
        either a class or an instance.
        """
        return value


class EmbeddedObjectProperty(Property):
    def __init__(self, type, **kwargs):
        self.type = type
        super(EmbeddedObjectProperty, self).__init__(**kwargs)

    def clean(self, value):
        if isinstance(self.type, _OpenC2Base) and isinstance(
            self.type, Property
        ):  # is a Custom Property
            return self.type.clean(value)
        elif type(value) is dict:
            value = self.type(**value)
        elif not isinstance(value, self.type):
            raise ValueError("must be of type {}.".format(self.type.__name__))
        return value


class ListProperty(Property):
    def __init__(self, contained, **kwargs):
        """
        ``contained`` should be a function which returns an object from the value.
        """
        if inspect.isclass(contained) and issubclass(contained, Property):
            # If it's a class and not an instance, instantiate it so that
            # clean() can be called on it, and ListProperty.clean() will
            # use __call__ when it appends the item.
            self.contained = contained()
        else:
            self.contained = contained
        super(ListProperty, self).__init__(**kwargs)

    def clean(self, value):
        try:
            iter(value)
        except TypeError:
            raise ValueError("must be an iterable.")

        if isinstance(value, (_OpenC2Base, (str,))):
            value = [value]

        result = []
        for item in value:
            try:
                valid = self.contained.clean(item)
            except ValueError:
                raise
            except AttributeError:
                # type of list has no clean() function (eg. built in Python types)
                # TODO Should we raise an error here?
                valid = item

            if type(self.contained) is EmbeddedObjectProperty:
                obj_type = self.contained.type
            elif type(self.contained) is DictionaryProperty:
                obj_type = dict
            else:
                obj_type = self.contained

            if isinstance(valid, Mapping):
                try:
                    valid._allow_custom
                except AttributeError:
                    result.append(obj_type(**valid))
                else:
                    result.append(obj_type(allow_custom=True, **valid))
            else:
                result.append(obj_type(valid))

        return result


class StringProperty(Property):
    def __init__(self, **kwargs):
        super(StringProperty, self).__init__(**kwargs)

    def clean(self, value):
        if not isinstance(value, str):
            return str(value)
        return value


class EnumProperty(StringProperty):
    def __init__(self, allowed, **kwargs):
        if type(allowed) is not list:
            raise ValueError("allowed must be a list")
        self.allowed = allowed
        super(EnumProperty, self).__init__(**kwargs)

    def clean(self, value):
        cleaned_value = super(EnumProperty, self).clean(value)
        if cleaned_value not in self.allowed:
            raise ValueError(
                "value '{}' is not valid for this enumeration.".format(cleaned_value)
            )

        return cleaned_value


class BinaryProperty(Property):
    def clean(self, value):
        try:
            base64.b64decode(value)
        except (binascii.Error, TypeError):
            raise ValueError("must contain a base64 encoded string")
        return value


class IntegerProperty(Property):
    def __init__(self, min=None, max=None, **kwargs):
        self.min = min
        self.max = max
        super(IntegerProperty, self).__init__(**kwargs)

    def clean(self, value):
        try:
            value = int(value)
        except Exception:
            raise ValueError("must be an integer.")

        if self.min is not None and value < self.min:
            msg = "minimum value is {}. received {}".format(self.min, value)
            raise ValueError(msg)

        if self.max is not None and value > self.max:
            msg = "maximum value is {}. received {}".format(self.max, value)
            raise ValueError(msg)

        return value


class DateTimeProperty(IntegerProperty):
    """
    Value is the number of milliseconds since 00:00:00 UTC, 1 January 1970
    """

    def __init__(self, **kwargs):
        super(DateTimeProperty, self).__init__(**kwargs)

    def clean(self, value):
        if isinstance(value, datetime.datetime):
            value = value.astimezone(datetime.timezone.utc)
            return super(DateTimeProperty, self).clean(value.timestamp() * 1000)

        value = super(DateTimeProperty, self).clean(value)
        self.datetime(value)
        return value

    def datetime(self, value):
        return datetime.datetime.utcfromtimestamp(value / 1000.0)


class FloatProperty(Property):
    def __init__(self, min=None, max=None, **kwargs):
        self.min = min
        self.max = max
        super(FloatProperty, self).__init__(**kwargs)

    def clean(self, value):
        try:
            value = float(value)
        except Exception:
            raise ValueError("must be a float.")

        if self.min is not None and value < self.min:
            msg = "minimum value is {}. received {}".format(self.min, value)
            raise ValueError(msg)

        if self.max is not None and value > self.max:
            msg = "maximum value is {}. received {}".format(self.max, value)
            raise ValueError(msg)

        return value


class DictionaryProperty(Property):
    def __init__(self, allowed_keys=None, allowed_key_regex=None, **kwargs):
        self.allowed_keys = allowed_keys
        self.allowed_key_regex = allowed_key_regex
        super(DictionaryProperty, self).__init__(**kwargs)

    def clean(self, value):
        try:
            dictified = utils._get_dict(value)
        except ValueError:
            raise ValueError("The dictionary property must contain a dictionary")
        for k in dictified.keys():
            if self.allowed_keys and k not in self.allowed_keys:
                raise exceptions.DictionaryKeyError(k, "Key not allowed")
            if self.allowed_key_regex and not re.match(self.allowed_key_regex, k):
                msg = (
                    "contains characters other than lowercase a-z, "
                    "uppercase A-Z, numerals 0-9, hyphen (-), or "
                    "underscore (_)"
                )
                raise exceptions.DictionaryKeyError(k, msg)

        return dictified


class PayloadProperty(Property):
    def clean(self, value):
        from .v10.common import Payload

        obj = Payload(**value)

        return obj


class ProcessProperty(Property):
    def clean(self, value):
        from .v10.targets import Process

        if value.get("process"):
            process = Process(**value.get("process"))
        else:
            process = Process(**value)
        return process


class FileProperty(Property):
    def __init__(self, required=False, fixed=None, default=None, version="1.0"):
        super(FileProperty, self).__init__(
            required=required, fixed=fixed, default=default
        )
        self._version = version

    def clean(self, value):
        if self._version == "1.0":
            from .v10.targets import File

            if value.get("file"):
                file = File(**value.get("file"))
            else:
                file = File(**value)
            return file
        return value


# openc2 1.0 spec only supports md5, sha1, sha256
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
                    raise ValueError(
                        "'{0}' is not a valid {1} hash".format(v, vocab_key)
                    )
                if k != vocab_key:
                    clean_dict[vocab_key] = clean_dict[k]
                    del clean_dict[k]
            else:
                raise ValueError("'{1}' is not a valid hash".format(v, k))
        if len(clean_dict) < 1:
            raise ValueError("must not be empty.")
        return clean_dict


class ComponentProperty(Property):
    def __init__(self, component_type=None, allow_custom=False, *args, **kwargs):
        super(ComponentProperty, self).__init__(*args, **kwargs)
        self.allow_custom = allow_custom
        self._component_type = component_type

    def clean(self, value):
        if not self._component_type:
            raise ValueError("This property requires a component type")
        dictified = {}
        try:
            if isinstance(value, _OpenC2Base):
                dictified[value._type] = utils._get_dict(value)
            else:
                dictified = utils._get_dict(value)
        except ValueError:
            raise ValueError("This property may only contain a dictionary or object")
        parsed_obj = utils.parse_component(
            dictified,
            allow_custom=self.allow_custom,
            component_type=self._component_type,
        )
        return parsed_obj


class TargetProperty(ComponentProperty):
    def __init__(self, allow_custom=False, *args, **kwargs):
        super(TargetProperty, self).__init__(
            allow_custom=allow_custom, component_type="targets", *args, **kwargs
        )


class ActuatorProperty(ComponentProperty):
    def __init__(self, allow_custom=False, *args, **kwargs):
        super(ActuatorProperty, self).__init__(
            allow_custom=allow_custom, component_type="actuators", *args, **kwargs
        )


class ArgsProperty(DictionaryProperty):
    def __init__(self, allow_custom=True, *args, **kwargs):
        super(ArgsProperty, self).__init__(allow_custom, *args, **kwargs)
        self.allow_custom = allow_custom

    def clean(self, value):
        dictified = {}
        try:
            dictified = utils._get_dict(value)
        except ValueError:
            raise ValueError("This property may only contain a dictionary or object")
        parsed_obj = utils.parse_args(dictified, allow_custom=self.allow_custom)
        return parsed_obj


def CustomProperty(type="x-acme", properties=None, version="1.0"):
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
        return _custom_property_builder(cls, type, _properties, version)

    return wrapper
