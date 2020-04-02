import openc2
import pytest
import json
import sys
import datetime


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


def test_binary_property():
    foo = openc2.properties.BinaryProperty()
    assert foo.clean("RXZlcldhdGNo") == "RXZlcldhdGNo"

    with pytest.raises(ValueError):
        foo.clean("bad")


def test_integer_property():
    foo = openc2.properties.IntegerProperty()
    assert foo.clean(1) == 1

    invalid = ["a"]
    for i in invalid:
        with pytest.raises(ValueError):
            foo.clean(i)

    foo = openc2.properties.IntegerProperty(min=1)
    with pytest.raises(ValueError):
        foo.clean(0)

    foo = openc2.properties.IntegerProperty(max=10)
    with pytest.raises(ValueError):
        foo.clean(11)


def test_float_property():
    foo = openc2.properties.FloatProperty()
    assert foo.clean(1.0) == 1.0
    assert foo.clean(1) == 1.0
    with pytest.raises(ValueError):
        foo.clean("a")

    foo = openc2.properties.FloatProperty(min=1.0)
    with pytest.raises(ValueError):
        foo.clean(0.0)

    foo.clean(1.0)

    foo = openc2.properties.FloatProperty(max=10.0)
    with pytest.raises(ValueError):
        foo.clean(11.0)


def test_dictionary_property():
    foo = openc2.properties.DictionaryProperty()
    assert foo.clean({"key": "value"}) == {"key": "value"}

    with pytest.raises(ValueError):
        foo.clean("bad")

    foo = openc2.properties.DictionaryProperty(allowed_keys=["key"])
    assert foo.clean({"key": "value"}) == {"key": "value"}

    try:
        foo.clean({"bad": "value"})
    except Exception as e:
        assert "Invalid dictionary key" in str(e)

    foo = openc2.properties.DictionaryProperty(allowed_key_regex=r"^[a-zA-Z0-9_-]+$")
    with pytest.raises(openc2.exceptions.DictionaryKeyError):
        foo.clean({"😈": "bad"})


def test_file_property():
    foo = openc2.properties.FileProperty()
    assert foo.clean({"name": "file.txt"}) == openc2.v10.targets.File(name="file.txt")

    foo = openc2.properties.FileProperty(version="0.0")
    assert foo.clean("bad") == "bad"


def test_component_property():
    foo = openc2.properties.ComponentProperty()
    with pytest.raises(ValueError):
        foo.clean({"key": "value"})

    foo = openc2.properties.ComponentProperty(component_type="bad_type")
    with pytest.raises(openc2.exceptions.CustomContentError):
        foo.clean({"key": "value"})

    with pytest.raises(ValueError):
        foo.clean("bad")


def test_datetime_property():
    foo = openc2.properties.DateTimeProperty()
    assert foo.clean(1) == 1
    assert (
        foo.clean(
            datetime.datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
        )
        == 0
    )
    assert (
        foo.clean(
            datetime.datetime(1970, 1, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        )
        == 3.6e6
    )
    assert (
        foo.clean(
            datetime.datetime(1970, 1, 1, 0, 1, 0, 0, tzinfo=datetime.timezone.utc)
        )
        == 60000
    )
    assert (
        foo.clean(
            datetime.datetime(1970, 1, 1, 0, 0, 1, 0, tzinfo=datetime.timezone.utc)
        )
        == 1000
    )
    assert (
        foo.clean(
            datetime.datetime(1970, 1, 1, 0, 0, 0, 1000, tzinfo=datetime.timezone.utc)
        )
        == 1
    )

    assert (
        foo.clean(
            datetime.datetime(1960, 1, 1, 0, 0, 0, 1000, tzinfo=datetime.timezone.utc)
        )
        == -315619199999
    )
    assert (
        foo.clean(
            datetime.datetime(
                1969, 12, 31, 23, 59, 59, 999000, tzinfo=datetime.timezone.utc
            )
        )
        == -1
    )

    assert foo.datetime(0) == datetime.datetime(1970, 1, 1, 0, 0, 0, 0)

    with pytest.raises(ValueError):
        foo.clean(sys.maxsize)

    with pytest.raises(ValueError):
        foo.datetime(sys.maxsize)


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

    bar = openc2.properties.EmbeddedObjectProperty(foo)

    assert bar.clean({"custom": "fixed_value"}) == {"custom": "fixed_value"}
    with pytest.raises(ValueError):
        bar.clean({"custom": "bad"})

    with pytest.raises(ValueError):
        bar.clean({"bad": "fixed_value"})

    @openc2.properties.CustomProperty("x-custom", [("custom", bar)])
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
