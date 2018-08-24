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
    """Class for OpenC2 Message

    Attributes:
        header (OpenC2Header): Information associated with an OpenC2 command or response
        body (OpenC2Command, OpenC2Response): The message payload, either
            OpenC2Command or OpenC2Response
    """
    def __init__(self, header=None, body=None):
        self.header = header
        self.body = body

class OpenC2Header(object):
    """Class for OpenC2 Header

    Attributes:
        version (str): Message protocol version
        id (str, UUID, optional): An identifier used to correlate responses to a command
        created (str, optional): Date and time the message was created
        sender (str, optional): Date and time the message was created
        content_type (str): The type and version of the message body

    """
    def __init__(self, version=__version__, id=None, created=None, sender=None,
                 content_type='application/json'):
        self.version = version
        self.id = id
        self.created = created
        self.sender = sender
        self.content_type = content_type

class OpenC2Target(OpenC2CommandField):
    """Class for OpenC2 Target

    Attributes:
        _name(str): The name of the object of the action
        _specifiers(str, AttributeDict): Further identifies the target
             to some level of precision, such as a specific target,
             a list of targets, or a class of targets.
    """
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
    """Class for OpenC2 Actuator

    Attributes:
        _name(str): The name of the set of functions performed by
            the actuator, and the name of the profile defining
            commands applicable to those functions.
        _specifiers(AttributeDict): The specifier identifies the
            actuator to some level of precision, such as a
            specific actuator, a list of actuators, or a group of
            actuators.
    """
    def __init__(self, _name, **kwargs):
        super(OpenC2Actuator, self).__init__(_name)
        if kwargs:
            self._specifiers = AttributeDict()
            for k,v in six.iteritems(kwargs):
                self._specifiers[k] = v

"""Alias for OpenC2Args class"""
OpenC2Args = AttributeDict

class OpenC2Command(object):
    """Class for OpenC2 Command

    Attributes:
        action (str): The task or activity to be performed
        target (OpenC2Target): The object of the action. The action is
            performed on the target.
        id (str, optional): The subject of the action. The actuator
            executes the action on the target.
        actuator (OpenC2Actuator, optional): An object containing
            additional properties that apply to the command
        args (OpenC2Args, dict, AttributeDict, optional): Identifier
            used to link responses to a command

    Raises:
        ValueError: If missing any required fields
    """
    def __init__(self, action, target, id=None, actuator=None, args={}):
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
        elif k == 'args':
           if isinstance(v, (AttributeDict, dict)):
               v = OpenC2Args(v)
           elif not isinstance(v, (OpenC2Args, type(None))):
               raise TypeError("args must be OpenC2Args, dict or None")
        super(OpenC2Command, self).__setattr__(k, v)

class OpenC2Response(object):
    """Class for OpenC2 Response

    Attributes:
        id (str): ID of the response
        id_ref (str): ID of the command that induced this response
        status (int): An integer status code
        status_text (str, optional): A free-form human-readable
            description of the response status
        results (str, optional): Data or extended status information
            that was requested from an OpenC2 Command
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
        elif k == 'status' and not isinstance(v, six.integer_types):
           raise TypeError("%s must be a string or integer " % k)
        elif k == 'status_text' and not isinstance(v, (six.string_types, type(None))):
           raise TypeError("%s must be a string or None" % k)
        super(OpenC2Response, self).__setattr__(k, v)
