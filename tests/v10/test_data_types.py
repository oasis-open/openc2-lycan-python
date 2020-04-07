import openc2
import pytest


def test_payload():
    foo = openc2.v10.Payload(url="https://everwatchsolutions.com/payload.exe")
    assert foo.url == "https://everwatchsolutions.com/payload.exe"

    with pytest.raises(openc2.exceptions.MutuallyExclusivePropertiesError):
        openc2.v10.Payload(
            url="https://everwatchsolutions.com/payload.exe", bin="RXZlcldhdGNo"
        )


def test_artifact():
    with pytest.raises(openc2.exceptions.AtLeastOnePropertyError):
        openc2.v10.Artifact()
