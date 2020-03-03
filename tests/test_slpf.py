import openc2
import pytest
import json
import sys
import stix2.exceptions


def test_slpf_actuator():
    foo = openc2.SLPFActuator(hostname="hostname")
    assert foo
    assert foo.hostname == "hostname"

    with pytest.raises(stix2.exceptions.ExtraPropertiesError):
        foo = openc2.SLPFActuator(bad="bad")

    foo = openc2.SLPFActuator(named_group="named_group")
    assert foo != None
    assert foo.named_group == "named_group"

    foo = openc2.SLPFActuator(asset_id="asset_id")
    assert foo != None
    assert foo.asset_id == "asset_id"

    # with the current specification SLPFActuator does not need any elements
    # and an empty asset_tuple is None
    foo = openc2.SLPFActuator(asset_tuple=[])
    assert foo != None

    with pytest.raises(AttributeError):
        foo.asset_tuple

    # check that there is less than 10
    for s in range(1, 10):
        values = list(map(lambda x: str(x), list(range(s))))
        f = openc2.SLPFActuator(asset_tuple=values)
        assert f.asset_tuple == values

    # max 10 items
    with pytest.raises(stix2.exceptions.InvalidValueError):
        openc2.SLPFActuator(asset_tuple=list(map(lambda x: str(x), list(range(11)))))


def test_slpf_cmd():
    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        openc2.v10.slpf.SLPF()

    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        openc2.v10.slpf.SLPF(action="query")

    with pytest.raises(stix2.exceptions.MissingPropertiesError):
        openc2.v10.slpf.SLPF(target=openc2.Features())

    foo = openc2.v10.slpf.SLPF(action="query", target=openc2.Features())
    assert foo != None
    assert foo.action == "query"

    with pytest.raises(stix2.exceptions.InvalidValueError):
        openc2.v10.slpf.SLPF(action="create", target=openc2.Features())

    with pytest.raises(ValueError):
        openc2.v10.slpf.SLPF(action="query", target=openc2.v10.targets.URI(uri="uri"))

    foo = openc2.v10.slpf.SLPF(
        action="query",
        target=openc2.Features(),
        actuator=openc2.SLPFActuator(hostname="hostname"),
    )
    assert foo != None
    assert foo.action == "query"
    assert foo.actuator.hostname == "hostname"

    @openc2.CustomActuator("x-thing", [("id", stix2.properties.StringProperty())])
    class MyCustomActuator(object):
        pass

    with pytest.raises(ValueError):
        openc2.v10.slpf.SLPF(
            action="query", target=openc2.Features(), actuator=MyCustomActuator(id="id")
        )
