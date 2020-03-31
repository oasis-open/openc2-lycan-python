import openc2
import pytest
import json
import sys


def test_hash_property():
    foo = openc2.properties.HashesProperty()
    with pytest.raises(ValueError):
        assert foo.clean({})
    assert foo.clean({"md5": "9AC6EC101ABD3F40A5C74B38038E1E20"})
    with pytest.raises(ValueError):
        foo.clean({"md5": "bad-hash"})
    with pytest.raises(ValueError):
        foo.clean({"bad": "value"})
