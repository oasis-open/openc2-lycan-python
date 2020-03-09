import openc2
import pytest
import json
import sys
import stix2.exceptions


def test_args_custom_property():


    with pytest.raises(stix2.exceptions.PropertyPresenceError):
        @openc2.properties.CustomProperty(
            "x-custom-property", [("value", stix2.properties.StringProperty())]
        )
        class MyCustomProp(object):
            pass

    with pytest.raises(stix2.exceptions.PropertyPresenceError):
        @openc2.properties.CustomProperty(
            "x-custom-property", [("type", stix2.properties.StringProperty())]
        )
        class MyCustomProp(object):
            pass
