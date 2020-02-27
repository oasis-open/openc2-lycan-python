import openc2
import pytest
import json
import stix2.exceptions


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


def test_features_unique():
    # A Producer MUST NOT send a list containing more than one instance of any Feature.
    # items must be unique
    with pytest.raises(stix2.exceptions.InvalidValueError):
        openc2.v10.Features(["versions"] * 2)


def test_features_size():
    for s in range(10):
        openc2.v10.Features(list(map(lambda x: str(x), list(range(s)))))

    # max 10 items
    with pytest.raises(stix2.exceptions.InvalidValueError):
        openc2.v10.Features(list(map(lambda x: str(x), list(range(11)))))
