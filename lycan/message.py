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

from lycan import __version__, AttributeDict, OpenC2CommandField
import uuid, six

class OpenC2Message(object):
    def __init__(self, header=None, body=None):
        self.header = header
        self.body = body

class OpenC2Header(object):
    def __init__(self, version=__version__, id=None, created=None, sender=None,
                 content_type='application/json'):
        self.version = version
        self.id = id
        self.created = created
        self.sender = sender
        self.content_type = content_type

class OpenC2Target(OpenC2CommandField):
    def __init__(self, _name, *args, **kwargs):
        super(OpenC2Target, self).__init__(_name)
        if args and len(args) == 1 and isinstance(args[0], six.string_types):
            self._specifiers = args[0]
        elif kwargs:
            self._specifiers = AttributeDict()
            for k,v in six.iteritems(kwargs):
                self._specifiers[k] = v
        else:
            self._specifiers = None

class OpenC2Actuator(OpenC2CommandField):
    def __init__(self, _name, **kwargs):
        super(OpenC2Actuator, self).__init__(_name)
        if kwargs:
            self._specifiers = AttributeDict()
            for k,v in six.iteritems(kwargs):
                self._specifiers[k] = v

OpenC2Args = AttributeDict

class OpenC2Command(object):
    """Class for OpenC2 Command

    Attributes:
        action (str): Action
        target (:OpenC2Target): Target
        id (str, optional): Command-ID
        actuator (:OpenC2Actuator, optional): Actuator
        args (:AttributeDict, optional): Command-Args

    Raises:
        ValueError: If missing any required fields
    """
    def __init__(self, action, target, id=None, actuator=None, args=None):
        super(OpenC2Command, self).__init__()
        self.action = action
        self.target = target
        self.id = id
        self.actuator = actuator
        self.args = args

    def __setattr__(self, k, v):
        if k == 'target' and not isinstance(v, OpenC2Target):
           raise TypeError("target must be OpenC2Target or str")
        elif k == 'actuator' and not isinstance(v, (OpenC2Actuator, type(None))):
           raise TypeError("actuator must be OpenC2Actuator or None")
        elif k == 'action' and not isinstance(v, six.string_types):
           raise TypeError("action must be str")
        elif k == 'id' and not isinstance(v, (uuid.UUID, six.string_types, type(None))):
           raise TypeError("id must be str or None")
        elif k == 'args' and not isinstance(v, (OpenC2Args, type(None))):
           raise TypeError("args must be OpenC2Args or None")
        else:
           super(OpenC2Command, self).__setattr__(k, v)

class OpenC2Response(object):
    """Class for OpenC2 Response

    Attributes:
        id (str): Command-ID
        id_ref (str): Command-ID reference
        status (str): Request status
        status_text (str, optional): Free-form description
        results (str, optional): Result string
    """
    def __init__(self, id, id_ref, status,
                 status_text=None, results=None):
        super(OpenC2Response, self).__init__()
        self.id = id
        self.id_ref = id_ref
        self.status = status
        self.status_text = status_text
        self.results = results

    def __setattr__(self, k, v):
        if k in ['id', 'id_ref'] and not isinstance(v, (uuid.UUID, six.string_types)):
           raise TypeError("%s must be a string" % k)
        elif k == 'status' and not isinstance(v, (six.string_types, six.integer_types)):
           raise TypeError("%s must be a string or integer " % k)
        elif k == 'status_text' and not isinstance(v, (six.string_types, type(None))):
           raise TypeError("%s must be a string or None" % k)
        else:
           super(OpenC2Response, self).__setattr__(k, v)
