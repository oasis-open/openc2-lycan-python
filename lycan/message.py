#
#  The MIT License (MIT)
#
# Copyright 2018 AT&T Intellectual Property. All other rights reserved.
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
.. module: lycan.message
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

from lycan import __version__

class OpenC2Message(object):
    """ Base class for OpenC2 message types """
    def __init__(self):
        self.version = __version__

class AttributeDict(dict):
    """Support accessing dictionary elements as attributes"""
    def __getattr__(self, k):
        if k not in self:
            return None
        return self[k]
    def __setattr__(self, k, v):
        self[k] = v
    def __delattr__(self, k):
        if k in self:
            del self[k]

class OpenC2CommandField(object):
    """Class for Command Target/Actuator

    Note:
        Define any class attributes as private, public attributes are assumed to be specifiers

    Attributes:
        _type (str): target/actuator type
        _specifiers (:AttributeDict, optional): target/actuator specifiers

    Raises:
        TypeError: If required `type` is missing
    """
    def __init__(self, _type):
        if isinstance(_type, dict):
            if 'type' not in _type:
                raise ValueError("Invalid OpenC2 field: type required")
            self._type = _type.pop('type')
            self._specifiers = AttributeDict(_type)
        elif isinstance(_type, str):
            self._type = _type
            self._specifiers = AttributeDict()
        else:
            raise TypeError("_type must be dict or str")

        self._type = self.get_datamodel(self._type)

    def get_datamodel(self, _type):
        """Build fully-qualified datamodel"""
        try:
            datamodel, _ = _type.split(':')
        except ValueError:
            return 'openc2:' + _type
        else:
            return _type

    def __setattr__(self, k, v):
        if k.startswith('_'):
            super(OpenC2CommandField, self).__setattr__(k, v)
        else:
            setattr(self._specifiers, k, v)

    def __getattr__(self, k):
        return getattr(self._specifiers, k)

    def __repr__(self):
        return self._type

    def __eq__(self, other):
        return str(self._type) == self.get_datamodel(other)

    def __ne__(self, other):
        return str(self._type) != self.get_datamodel(other)

    @property
    def specifiers(self):
        """dict: Specifiers dictionary"""
        return self._specifiers

class OpenC2Command(OpenC2Message):
    """Class for OpenC2 Command

    Attributes:
        action (str): Action
        target (:OpenC2CommandField): Target
        actuator (:OpenC2CommandField, optional): Actuator
        modifiers (:AttributeDict, optional): Modifiers

    Raises:
        ValueError: If missing any required fields
    """
    def __init__(self, action, target, actuator=None, modifiers={}):
        super(OpenC2Command, self).__init__()
        self.action = action
        self.target = OpenC2CommandField(target)
        self.actuator = None if actuator == None else OpenC2CommandField(actuator)
        self.modifiers = AttributeDict(modifiers)

class OpenC2Response(OpenC2Message):
    """Class for OpenC2 Response

    Attributes:
        source (str): Command source
        status (str): Request status
        results (str): Result string
        cmdref (str, optional): Command reference
        status_text (str, optional): Free-form description
    """
    def __init__(self, source, status, results,
                 cmdref=None, status_text=None):
        super(OpenC2Response, self).__init__()
        self.source = source
        self.status = status
        self.results = results
        self.cmdref = cmdref
        self.status_text = status_text
