import openc2
import pytest
import json
import sys


def test_response_create():
    with pytest.raises(openc2.exceptions.MissingPropertiesError):
        openc2.v10.Response()

    with pytest.raises(openc2.exceptions.MissingPropertiesError):
        openc2.v10.Response(results={})

    with pytest.raises(openc2.exceptions.MissingPropertiesError):
        openc2.v10.Response(status_text="Ok.")

    foo = openc2.v10.Response(status=200)
    assert foo
    assert foo.status == 200
    assert foo.serialize() == '{"status": 200}'

    bar = openc2.v10.Response(**json.loads(foo.serialize()))
    assert bar == foo

    bar = openc2.parse({"status": 200})
    assert foo == bar

    bar = openc2.parse(foo.serialize())
    assert foo == bar
