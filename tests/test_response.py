import openc2
import pytest
import json
import sys
import stix2


def test_response_create():
    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        openc2.Response()

    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        openc2.Response(results={})

    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        openc2.Response(status_text="Ok.")

    foo = openc2.Response(status=200)
    assert foo
    assert foo.status == 200
    assert foo.serialize() == '{"status": 200}'

    bar = openc2.Response(**json.loads(foo.serialize()))
    assert bar == foo

    bar = openc2.parse({"status": 200})
    assert foo == bar

    bar = openc2.parse(foo.serialize())
    assert foo == bar
