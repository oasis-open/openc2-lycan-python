import openc2
import pytest
import json
import sys
import stix2.exceptions


def test_args_custom_invalid_property():

    with pytest.raises(stix2.exceptions.PropertyPresenceError):

        @openc2.properties.CustomProperty(
            "x-custom-property", [("type", stix2.properties.StringProperty())]
        )
        class MyCustomProp(object):
            pass

    with pytest.raises(TypeError):

        @openc2.properties.CustomProperty("x-custom-property", None)
        class MyCustomProp(object):
            pass

    with pytest.raises(ValueError):

        @openc2.properties.CustomProperty("x-custom-property", [])
        class MyCustomProp(object):
            pass


def test_args_custom_embed_property():
    @openc2.properties.CustomProperty(
        "x-custom-property-inner", [("value", stix2.properties.StringProperty())]
    )
    class MyCustomPropInner(object):
        pass

    @openc2.properties.CustomProperty(
        "x-custom-property",
        [("value", stix2.properties.ListProperty(MyCustomPropInner))],
    )
    class MyCustomProp(object):
        pass

    foo = MyCustomProp(value=[{"value": "my_value"}])
    assert foo != None
    assert len(foo.value) > 0
    assert foo.value[0] != None
    assert foo.value[0].value == "my_value"

    bar = foo(_value=foo)
    assert bar == foo

    foo = MyCustomProp(value=[MyCustomPropInner(value="my_value")])
    assert foo != None
    assert len(foo.value) > 0
    assert foo.value[0] != None
    assert foo.value[0].value == "my_value"

    foo2 = MyCustomProp(value=[MyCustomPropInner(value="my_value2")])
    assert foo2 != None
    assert len(foo2.value) > 0
    assert foo2.value[0] != None
    assert foo2.value[0].value == "my_value2"

    assert foo != foo2

    @openc2.CustomArgs(
        "x-custom", [("value", stix2.properties.ListProperty(MyCustomProp))]
    )
    class MyCustomArgs(object):
        pass

    bar = MyCustomArgs(value=[foo])
    assert bar != None
    assert len(foo.value) > 0
    assert bar.value[0] != None
    assert len(bar.value[0].value) > 0
    assert bar.value[0].value[0] != None
    assert bar.value[0].value[0].value == "my_value"

    bar = MyCustomArgs(value=[foo, foo2])
    print('bar', bar.serialize())
    assert bar != None
    assert len(foo.value) > 0
    assert bar.value[0] != None
    assert len(bar.value[0].value) > 0
    assert bar.value[0].value[0] != None
    assert bar.value[0].value[0].value == "my_value"
    assert bar.value[1].value[0] != None
    assert bar.value[1].value[0].value == "my_value2"
