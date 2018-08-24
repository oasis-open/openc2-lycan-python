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
.. module: lycan
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

import six

__version__ = '0.1.0'

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
    """Base Class for Command Target/Actuator

    Attributes:
        _name (str): target/actuator name
        _specifiers (AttributeDict, optional): target/actuator specifiers

    Raises:
        TypeError: If required `name` is missing
    """
    def __init__(self, _name):
        self._name = _name
        self._specifiers = None

    def __setattr__(self, k, v):
        if k.startswith('_'):
            super(OpenC2CommandField, self).__setattr__(k, v)
        else:
            if not self._specifiers:
                if k == self._name:
                    self._specifiers = v
                else:
                    self._specifiers = AttributeDict()
                    setattr(self._specifiers, k, v)
            else:
                setattr(self._specifiers, k, v)

    def __getattr__(self, k):
        if isinstance(self._specifiers, six.string_types):
            return self._specifiers
        return getattr(self._specifiers, k)

    def __repr__(self):
        return self._name

    def __eq__(self, other):
        return str(self._name) == other

    def __ne__(self, other):
        return str(self._name) != other

    @property
    def specifiers(self):
        """dict: Specifiers dictionary"""
        return self._specifiers
