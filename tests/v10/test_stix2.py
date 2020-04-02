import openc2
import stix2
import pytest
import json


def test_custom_target():
    @openc2.v10.CustomTarget("x-thing:id", [("id", stix2.properties.StringProperty())])
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
            "x-invalid", [("id", stix2.properties.StringProperty())]
        )
        class CustomTargetInvalid(object):
            pass

    with pytest.raises(ValueError):

        @openc2.v10.CustomTarget(
            "invalid_target", [("id", stix2.properties.StringProperty())]
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
            "x-custom:id", ("id", stix2.properties.StringProperty()),
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


def test_stix2_indicator():
    indicator = stix2.Indicator(
        name="File hash for malware variant",
        labels=["malicious-activity"],
        pattern="[file:hashes.md5 = 'd41d8cd98f00b204e9800998ecf8427e']",
    )

    foo = openc2.v10.Args(indicator=indicator, allow_custom=True)
    assert '"name": "File hash for malware variant"' in foo.serialize()
    assert '"labels": ["malicious-activity"]' in foo.serialize()
    assert (
        '"pattern": "[file:hashes.md5 = \'d41d8cd98f00b204e9800998ecf8427e\']"'
        in foo.serialize()
    )

    # an indicator isn't a property so we have to embed it
    @openc2.v10.args.CustomArgs(
        "x-indicator-args",
        [("indicator", openc2.properties.EmbeddedObjectProperty(stix2.Indicator))],
    )
    class CustomIndicatorArgs(object):
        pass

    foo = CustomIndicatorArgs(indicator=indicator)
    assert '"name": "File hash for malware variant"' in foo.serialize()
    assert '"labels": ["malicious-activity"]' in foo.serialize()
    assert (
        '"pattern": "[file:hashes.md5 = \'d41d8cd98f00b204e9800998ecf8427e\']"'
        in foo.serialize()
    )
