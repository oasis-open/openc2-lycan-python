import openc2
import pytest

import stix2.exceptions


def test_args_simple():
    valid = ["none",
                "ack",
                "status",
                "complete"]
    for v in valid:
        a = openc2.v10.Args(response_requested=v)
        print(a)

    with pytest.raises(stix2.exceptions.InvalidValueError):
        openc2.v10.Args(response_requested="bad")
