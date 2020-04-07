import openc2
import pytest
import json


def test_features_empty():
    f = openc2.v10.Features()
    assert f.features == []

    f = openc2.v10.Features([])
    assert f.features == []

    f = openc2.v10.Features(None)
    assert f.features == []

    f = openc2.v10.Features(["pairs"])
    assert f.features
    assert f.features[0] == "pairs"

    f = openc2.v10.Features(["pairs", "versions"])
    assert f.features
    assert f.features[0] == "pairs"
    assert f.features[1] == "versions"

    with pytest.raises(openc2.exceptions.InvalidValueError):
        openc2.v10.Features(["invalid"])


def test_features_unique():
    # A Producer MUST NOT send a list containing more than one instance of any Feature.
    # items must be unique
    with pytest.raises(openc2.exceptions.InvalidValueError):
        openc2.v10.Features(["versions"] * 2)
