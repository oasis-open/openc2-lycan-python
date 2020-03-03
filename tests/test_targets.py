import openc2
import pytest
import json
import stix2


def test_ipv4_address_example():
    ip4 = openc2.v10.IPv4Address(ipv4_net="198.51.100.3")

    assert ip4.ipv4_net == "198.51.100.3"

    ser_ipv4 = json.loads(ip4.serialize())
    ip4_2 = openc2.v10.IPv4Address(**ser_ipv4)
    assert ip4 == ip4_2

    ip4 = openc2.v10.IPv4Address(ipv4_net="198.51.100.0/24")

    assert ip4.ipv4_net == "198.51.100.0/24"

    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        ip4 = openc2.v10.IPv4Address()

    assert excinfo.value.cls == openc2.v10.IPv4Address


def test_custom_target():
    @openc2.CustomTarget("x-thing:id", [("id", stix2.properties.StringProperty())])
    class CustomTarget(object):
        pass

    one = CustomTarget()
    assert one != None  # for some reason `assert one` fails

    with pytest.raises(stix2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    one = CustomTarget(id="uuid")
    assert one
    assert one.id == "uuid"

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    with pytest.raises(stix2.exceptions.ParseError):
        openc2.parse(one.serialize())


def test_multiple_custom_targets():
    @openc2.CustomTarget("x-thing:id", [("id", stix2.properties.StringProperty())])
    class CustomTarget(object):
        pass

    @openc2.CustomTarget("x-thing:name", [("name", stix2.properties.StringProperty())])
    class CustomTarget2(object):
        pass

    one = CustomTarget()
    assert one != None  # for some reason `assert one` fails

    with pytest.raises(stix2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    one = CustomTarget(id="uuid")
    assert one
    assert one.id == "uuid"

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    with pytest.raises(stix2.exceptions.ParseError):
        openc2.parse(one.serialize())

    foo = CustomTarget2()
    assert foo != None

    with pytest.raises(stix2.exceptions.ExtraPropertiesError):
        CustomTarget2(bad="id")

    one = CustomTarget2(name="name")
    assert one
    assert one.name == "name"

    two = CustomTarget2(name=(json.loads(one.serialize())["x-thing:name"]))
    assert one == two

    with pytest.raises(stix2.exceptions.ParseError):
        openc2.parse(one.serialize())


def test_custom_target_required():
    @openc2.CustomTarget(
        "x-thing:id", [("id", stix2.properties.StringProperty(required=True))]
    )
    class CustomTarget(object):
        pass

    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        CustomTarget()

    with pytest.raises(stix2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    one = CustomTarget(id="uuid")
    assert one
    assert one.id == "uuid"

    with pytest.raises(stix2.exceptions.ParseError):
        openc2.parse(one.serialize())

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two


def test_custom_target_with_custom_property():
    @openc2.properties.CustomProperty(
        "x-thing",
        [
            ("uid", stix2.properties.StringProperty()),
            ("name", stix2.properties.StringProperty()),
            ("version", stix2.properties.StringProperty()),
        ],
    )
    class CustomTargetProperty(object):
        pass

    @openc2.CustomTarget(
        "x-thing:id", [("id", CustomTargetProperty(required=True, default=lambda: {}))]
    )
    class CustomTarget(object):
        pass

    # no property
    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        CustomTarget()

    # empty property

    one = CustomTarget(id=CustomTargetProperty())
    assert one

    with pytest.raises(stix2.exceptions.ParseError):
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

    with pytest.raises(stix2.exceptions.ParseError):
        openc2.parse(one.serialize())

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    @openc2.CustomTarget(
        "x-thing:list",
        [("list", openc2.properties.EmptyListProperty(CustomTargetProperty))],
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
