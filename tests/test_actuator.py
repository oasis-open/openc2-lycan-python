import openc2
import pytest
import json
import sys


def test_actuator_requested():
    @openc2.v10.CustomActuator("x-thing", [("id", openc2.properties.StringProperty())])
    class MyCustomActuator(object):
        pass

    foo = MyCustomActuator(id="id")
    assert foo
    assert foo.id == "id"

    bar = openc2.utils.parse_actuator(json.loads(foo.serialize()))
    assert bar == foo

    with pytest.raises(ValueError):

        @openc2.v10.CustomActuator(
            "invalid_target", [("id", openc2.properties.StringProperty())]
        )
        class CustomInvalid(object):
            pass

    with pytest.raises(ValueError):

        @openc2.v10.CustomActuator(
            "over_16_chars_long_aaaaaaaaaaaaaaaaaaaa",
            [("id", openc2.properties.StringProperty())],
        )
        class CustomInvalid(object):
            pass

    with pytest.raises(ValueError):

        @openc2.v10.CustomActuator("x-thing:noprops", [])
        class CustomInvalid(object):
            pass
