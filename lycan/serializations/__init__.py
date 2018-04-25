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
from lycan.message import OpenC2Command,OpenC2Response


class OpenC2MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        message = {}
        if isinstance(obj, OpenC2Command):
            message["action"] = obj.action
            message["target"] = { "type": str(obj.target) }
            for (k,v) in six.iteritems(obj.target.specifiers):
                message["target"][k] = v
            if obj.actuator:
                message["actuator"] = { "type": str(obj.actuator) }
                for (k,v) in six.iteritems(obj.actuator.specifiers):
                    message["actuator"][k] = v
            if obj.modifiers:
                message["modifiers"] = obj.modifiers
        elif isinstance(obj, OpenC2Response):
            message["response"] = { "source": { "type": obj.source } }
            message["status"] = obj.status
            message["results"] = obj.results
            if obj.cmdref:
                message["cmdref"] = obj.cmdref
            if obj.status_text:
                message["status_text"] = obj.status_text
        else:
            raise ValueError("Invalid OpenC2 message")
        return message

class OpenC2MessageDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        message = obj
        if "action" in obj:
            if not "target" in obj:
                raise ValueError("Invalid OpenC2 command: target required")
            message = OpenC2Command(obj["action"], obj["target"], obj["actuator"] if "actuator" in obj else None,
                                       obj["modifiers"] if "modifiers" in obj else {})
        elif "response" in obj:
            if "source" in obj["response"]:
                if not "status" in obj:
                    raise ValueError("Invalid OpenC2 response: status required")
                if not "results" in obj:
                    raise ValueError("Invalid OpenC2 response: results required")
                message = OpenC2Response(obj["response"]["source"], obj["status"], obj["results"], obj["cmdref"] if "cmdref" in obj else None,
                                       obj["status_text"] if "status_text" in obj else None)
            else:
                raise ValueError("Invalid OpenC2 response: source required")
        return message
