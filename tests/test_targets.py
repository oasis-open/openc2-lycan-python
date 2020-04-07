import openc2
import pytest
import json


def test_ipv4_address_example():
    ip4 = openc2.v10.IPv4Address(ipv4_net="198.51.100.3")
    assert ip4.type == "ipv4_net"
    assert ip4["type"] == "ipv4_net"
    assert ip4.get("type") == "ipv4_net"

    with pytest.raises(AttributeError):
        ip4.bad

    with pytest.raises(openc2.exceptions.ImmutableError):
        ip4.type = "bad"

    try:
        ip4.type = "bad"
    except Exception as e:
        assert "Cannot modify" in str(e)

    assert ("%r" % ip4) == "IPv4Address(ipv4_net='198.51.100.3')"

    assert ip4.ipv4_net == "198.51.100.3"
    assert ip4["ipv4_net"] == "198.51.100.3"
    assert ip4.get("ipv4_net") == "198.51.100.3"

    assert len(ip4) == 1

    for prop in ip4:
        assert prop == "ipv4_net"

    ip4.ipv4_net = "198.51.100.32"
    assert ip4.ipv4_net == "198.51.100.32"

    assert ip4.serialize() == '{"ipv4_net": "198.51.100.3"}'
    assert ip4.serialize(pretty=True) == '{\n    "ipv4_net": "198.51.100.3"\n}'

    ser_ipv4 = json.loads(ip4.serialize())
    ip4_2 = openc2.v10.IPv4Address(**ser_ipv4)
    assert ip4 == ip4_2

    ip4 = openc2.v10.IPv4Address(ipv4_net="198.51.100.0/24")

    assert ip4.ipv4_net == "198.51.100.0/24"

    with pytest.raises(openc2.exceptions.MissingPropertiesError) as excinfo:
        ip4 = openc2.v10.IPv4Address()

    assert excinfo.value.cls == openc2.v10.IPv4Address

    bar = openc2.utils.parse_target(json.loads(ip4.serialize()))
    assert ip4 == bar


def test_custom_target():
    @openc2.v10.CustomTarget("x-thing:id", [("id", openc2.properties.StringProperty())])
    class CustomTarget(object):
        pass

    one = CustomTarget()
    assert one != None  # for some reason `assert one` fails

    with pytest.raises(openc2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    one = CustomTarget(id="uuid")
    assert one
    assert one.id == "uuid"

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    with pytest.raises(openc2.exceptions.ParseError):
        openc2.parse(one.serialize())

    with pytest.raises(ValueError):

        @openc2.v10.CustomTarget(
            "x-invalid", [("id", openc2.properties.StringProperty())]
        )
        class CustomTargetInvalid(object):
            pass

    with pytest.raises(ValueError):

        @openc2.v10.CustomTarget(
            "invalid_target", [("id", openc2.properties.StringProperty())]
        )
        class CustomTargetInvalid(object):
            pass

    with pytest.raises(ValueError):

        @openc2.v10.CustomTarget(
            "over_16_chars_long_aaaaaaaaaaaaaaaaaaaa123",
            [("id", openc2.properties.StringProperty())],
        )
        class CustomTargetInvalid(object):
            pass

    with pytest.raises(TypeError):

        @openc2.v10.CustomTarget(
            "x-custom:id", ("id", openc2.properties.StringProperty()),
        )
        class CustomTargetInvalid(object):
            pass

    with pytest.raises(TypeError):

        @openc2.v10.CustomTarget("x-custom:id")
        class CustomTargetInvalid(object):
            pass

    with pytest.raises(ValueError):

        @openc2.v10.CustomTarget(
            "x-over_16_chars_long_aaaaaaaaaaaaaaaaaaaa:id",
            [("id", openc2.properties.StringProperty())],
        )
        class CustomTargetInvalid(object):
            pass

    with pytest.raises(ValueError):

        @openc2.v10.CustomTarget("x-thing:noprops", [])
        class CustomTargetInvalid(object):
            pass

    with pytest.raises(openc2.exceptions.InvalidValueError):
        v = """{ "target": {"x-custom": "value"}, "action":"query"}"""
        openc2.utils.parse(v)

    with pytest.raises(openc2.exceptions.InvalidValueError):
        v = """{ "target": {"x-custom:id": "value"}, "action":"query"}"""
        openc2.utils.parse(v)

    with pytest.raises(openc2.exceptions.InvalidValueError):
        v = """{ "target": {}, "action":"query"}"""
        openc2.utils.parse(v)


def test_custom_target_embed():
    @openc2.properties.CustomProperty(
        "x-custom", [("custom", openc2.properties.StringProperty(fixed="custom"))]
    )
    class CustomProperty(object):
        pass

    @openc2.v10.CustomTarget(
        "x-thing:custom",
        [("custom", openc2.properties.EmbeddedObjectProperty(CustomProperty))],
    )
    class CustomTarget(object):
        pass

    foo = CustomTarget()
    assert foo != None

    with pytest.raises(openc2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    with pytest.raises(openc2.exceptions.InvalidValueError):
        bar = CustomProperty(custom="bad")

    bar = CustomProperty(custom="custom")
    foo = CustomTarget(custom=bar)
    assert foo

    assert foo.serialize() == '{"x-thing:custom": {"custom": "custom"}}'


def test_multiple_custom_targets():
    @openc2.v10.CustomTarget("x-thing:id", [("id", openc2.properties.StringProperty())])
    class CustomTarget(object):
        pass

    @openc2.v10.CustomTarget(
        "x-thing:name", [("name", openc2.properties.StringProperty())]
    )
    class CustomTarget2(object):
        pass

    one = CustomTarget()
    assert one != None  # for some reason `assert one` fails

    with pytest.raises(openc2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    one = CustomTarget(id="uuid")
    assert one
    assert one.id == "uuid"

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    with pytest.raises(openc2.exceptions.ParseError):
        openc2.parse(one.serialize())

    foo = CustomTarget2()
    assert foo != None

    with pytest.raises(openc2.exceptions.ExtraPropertiesError):
        CustomTarget2(bad="id")

    one = CustomTarget2(name="name")
    assert one
    assert one.name == "name"

    two = CustomTarget2(name=(json.loads(one.serialize())["x-thing:name"]))
    assert one == two

    with pytest.raises(openc2.exceptions.ParseError):
        openc2.parse(one.serialize())


def test_custom_target_required():
    @openc2.v10.CustomTarget(
        "x-thing:id", [("id", openc2.properties.StringProperty(required=True))]
    )
    class CustomTarget(object):
        pass

    with pytest.raises(openc2.exceptions.MissingPropertiesError):
        CustomTarget()

    with pytest.raises(openc2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    one = CustomTarget(id="uuid")
    assert one
    assert one.id == "uuid"

    with pytest.raises(openc2.exceptions.ParseError):
        openc2.parse(one.serialize())

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two


def test_custom_target_with_custom_property():
    @openc2.properties.CustomProperty(
        "x-thing",
        [
            ("uid", openc2.properties.StringProperty()),
            ("name", openc2.properties.StringProperty()),
            ("version", openc2.properties.StringProperty()),
        ],
    )
    class CustomTargetProperty(object):
        pass

    @openc2.v10.CustomTarget(
        "x-thing:id", [("id", CustomTargetProperty(required=True, default=lambda: {}))]
    )
    class CustomTarget(object):
        pass

    # no property
    with pytest.raises(openc2.exceptions.MissingPropertiesError):
        CustomTarget()

    # empty property

    one = CustomTarget(id=CustomTargetProperty())
    assert one

    with pytest.raises(openc2.exceptions.ParseError):
        openc2.parse(one.serialize())

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    # property with one value

    one = CustomTarget(id=CustomTargetProperty(name="name"))
    assert one != None
    assert one.id.name == "name"

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    # property with multiple values

    one = CustomTarget(
        id=CustomTargetProperty(name="name", uid="uid", version="version")
    )
    assert one.id.name == "name"
    assert one.id.uid == "uid"
    assert one.id.version == "version"

    with pytest.raises(openc2.exceptions.ParseError):
        openc2.parse(one.serialize())

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    @openc2.v10.CustomTarget(
        "x-thing:list",
        [("list", openc2.properties.ListProperty(CustomTargetProperty))],
    )
    class CustomTarget2(object):
        pass

    foo = CustomTarget2()
    assert foo != None

    foo = CustomTarget2(
        list=[CustomTargetProperty(name="name", uid="uid", version="version")]
    )
    assert foo != None
    assert foo.list != None
    assert foo.list[0] != None
    assert foo.list[0].name == "name"
    assert foo.list[0].uid == "uid"
    assert foo.list[0].version == "version"
