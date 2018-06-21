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
.. module: lycan.serializations
    :platform: Unix

.. version:: $$VERSION$$
.. moduleauthor:: Michael Stair <mstair@att.com>

"""

import six, json
from lycan.message import OpenC2Message, OpenC2Command, OpenC2Response, OpenC2Target, OpenC2Actuator, OpenC2Header

class OpenC2MessageEncoder(json.JSONEncoder):

    def _encode_message(self, obj, message):
        if obj.header:
            message["header"] = {}
            header = obj.header
            message["header"]["version"] = header.version
            if header.id:
                message["header"]["id"] = header.id
            if header.created:
                message["header"]["created"] = header.created
            if header.sender:
                message["header"]["sender"] = header.sender
            message["header"]["content_type"] = header.content_type
        if obj.body:
            body = obj.body
            if isinstance(body, OpenC2Command):
                message["command"] = {}
                self._encode_command(body, message["command"])
            elif isinstance(body, OpenC2Response):
                message["response"] = {}
                self._encode_response(body, message["response"])
            else:
                raise ValueError("Invalid OpenC2 message")
        else:
            raise ValueError("Invalid OpenC2 message")

    def _encode_command(self, obj, message):
        message["action"] = obj.action
        if isinstance(obj.target.specifiers, six.string_types):
            message["target"] = {str(obj.target): str(obj.target.specifiers)}
        else:
            target =  str(obj.target)
            message["target"] = {target: {}}
            if obj.target.specifiers:
                for (k, v) in six.iteritems(obj.target.specifiers):
                    message["target"][target][k] = v
        if obj.actuator:
            actuator = str(obj.actuator)
            message["actuator"] = {actuator: {}}
            if obj.actuator.specifiers:
                for (k, v) in six.iteritems(obj.actuator.specifiers):
                    message["actuator"][actuator][k] = v
        if obj.id:
            message["id"] = str(obj.id)
        if obj.args:
            message["args"] = obj.args

    def _encode_response(self, obj, message):
        message["id"] = obj.id
        message["id_ref"] = obj.id_ref
        message["status"] = obj.status
        if obj.status_text:
            message["status_text"] = obj.status_text
        if obj.results:
            message["results"] = obj.results

    def default(self, obj):
        message = {}
        if isinstance(obj, OpenC2Message):
            self._encode_message(obj, message)
        if isinstance(obj, OpenC2Command):
            self._encode_command(obj, message)
        if isinstance(obj, OpenC2Response):
            self._encode_response(obj, message)
        return message

class OpenC2MessageDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def _decode_message(self, obj):
        header = self._decode_header(obj["header"])
        if "command" in obj:
           body = obj["command"]
        elif "response" in obj:
           body = obj["response"]
        else:
           raise ValueError("Invalid OpenC2 message")
        return OpenC2Message(header, body)

    def _decode_header(self, obj):
        if "version" not in obj:
            raise ValueError("Invalid OpenC2 header: version required")
        if "content_type" not in obj:
            raise ValueError("Invalid OpenC2 header: content_type required")
        return OpenC2Header(obj["version"],
                            obj["command_id"] if "command_id" in obj else None,
                            obj["created"] if "created" in obj else None,
                            obj["sender"] if "sender" in obj else None,
                            obj["content_type"] if "content_type" in obj else None)

    def _decode_command(self, obj):
        if "target" not in obj:
            raise ValueError("Invalid OpenC2 command: target required")
        target_name = list(obj["target"].keys())[0]
        target_specifiers = list(obj["target"].values())[0]
        if isinstance(target_specifiers, dict):
            target = OpenC2Target(target_name, **target_specifiers)
        elif isinstance(target_specifiers, six.string_types):
            target = OpenC2Target(target_name, target_specifiers)
        else:
            raise ValueError("Invalid OpenC2 command target")

        actuator = None
        if "actuator" in obj:
            actuator_name = list(obj["actuator"].keys())[0]
            actuator_specifiers = list(obj["actuator"].values())[0]
            actuator = OpenC2Actuator(actuator_name, **actuator_specifiers)
        return OpenC2Command(obj["action"], target,
                             obj["id"] if "id" in obj else None,
                             actuator, obj["args"] if "args" in obj else {})

    def _decode_response(self, obj):
        if "id" not in obj:
            raise ValueError("Invalid OpenC2 response: id required")
        if "id_ref" not in obj:
            raise ValueError("Invalid OpenC2 response: id_ref required")
        if "status" not in obj:
            raise ValueError("Invalid OpenC2 response: status required")
        return OpenC2Response(obj["id"], obj["id_ref"], obj["status"],
                              obj["status_text"] if "status_text" in obj else None,
                              obj["results"] if "results" in obj else None)

    def object_hook(self, obj):
        if "header" in obj:
            message = self._decode_message(obj)
        elif "action" in obj:
            message = self._decode_command(obj)
        elif "id_ref" in obj:
            message = self._decode_response(obj)
        else:
            message = obj
        return message
