import openc2
import pytest
import json
import sys


def test_args_custom_invalid_property():

    with pytest.raises(openc2.exceptions.PropertyPresenceError):

        @openc2.properties.CustomProperty(
            "x-custom-property", [("type", openc2.properties.StringProperty())]
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
        "x-custom-property-inner", [("value", openc2.properties.StringProperty())]
    )
    class MyCustomPropInner(object):
        pass

    @openc2.properties.CustomProperty(
        "x-custom-property",
        [("value", openc2.properties.ListProperty(MyCustomPropInner))],
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

    @openc2.v10.CustomArgs(
        "x-custom", [("value", openc2.properties.ListProperty(MyCustomProp))]
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
    print("bar", bar.serialize())
    assert bar != None
    assert len(foo.value) > 0
    assert bar.value[0] != None
    assert len(bar.value[0].value) > 0
    assert bar.value[0].value[0] != None
    assert bar.value[0].value[0].value == "my_value"
    assert bar.value[1].value[0] != None
    assert bar.value[1].value[0].value == "my_value2"


def test_custom_property_fixed():
    @openc2.properties.CustomProperty(
        "x-custom-property", [("custom", openc2.properties.StringProperty())]
    )
    class MyCustomProp(object):
        pass

    foo = MyCustomProp(custom="custom_value")
    assert foo.serialize() == '{"custom": "custom_value"}'

    fixed = MyCustomProp(custom="fixed_value")

    foo = MyCustomProp(fixed=fixed)
    assert foo.serialize() == "{}"  # not required so can be empty

    @openc2.properties.CustomProperty(
        "x-custom", [("custom", openc2.properties.EmbeddedObjectProperty(foo))]
    )
    class EmbedCustomFixed(object):
        pass

    foo = EmbedCustomFixed()
    assert foo != None
    assert foo.serialize() == "{}"

    with pytest.raises(openc2.exceptions.InvalidValueError):
        EmbedCustomFixed(custom=MyCustomProp(custom="bad"))

    foo = EmbedCustomFixed(custom=fixed)
    assert foo.serialize() == '{"custom": {"custom": "fixed_value"}}'

    foo = EmbedCustomFixed(custom={"custom": "fixed_value"})
    assert foo.serialize() == '{"custom": {"custom": "fixed_value"}}'
