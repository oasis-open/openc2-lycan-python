import openc2
import pytest
import json

import stix2.exceptions


def test_args_response_requested():
    valid = ["none",
                "ack",
                "status",
                "complete"]
    for v in valid:
        a = openc2.v10.Args(response_requested=v)
        print(a)
        ser_a = json.loads(a.serialize())
        b = openc2.v10.Args(**ser_a)
        assert a == b


    with pytest.raises(stix2.exceptions.InvalidValueError):
        openc2.v10.Args(response_requested="bad")
