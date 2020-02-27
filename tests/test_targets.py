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
    assert one != None # for some reason `assert one` fails

    with pytest.raises(stix2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    one = CustomTarget(id="uuid")
    assert one
    assert one.id == "uuid"

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

def test_custom_target_required():
    @openc2.CustomTarget("x-thing:id", [("id", stix2.properties.StringProperty(required=True))])
    class CustomTarget(object):
        pass

    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        CustomTarget()

    with pytest.raises(stix2.exceptions.ExtraPropertiesError):
        CustomTarget(bad="id")

    one = CustomTarget(id="uuid")
    assert one
    assert one.id == "uuid"

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

    @openc2.CustomTarget("x-thing:id", [("id", CustomTargetProperty(required=True))])
    class CustomTarget(object):
        pass

    # no property
    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        CustomTarget()

    # empty property

    one = CustomTarget(id=CustomTargetProperty())
    assert one

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    # property with one value

    one = CustomTarget(id=CustomTargetProperty(name="name"))
    assert one.id.name == "name"

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two

    # property with multiple values

    one = CustomTarget(id=CustomTargetProperty(name="name", uid="uid", version="version"))
    assert one.id.name == "name"
    assert one.id.uid == "uid"
    assert one.id.version == "version"

    two = CustomTarget(id=(json.loads(one.serialize())["x-thing:id"]))
    assert one == two
