import openc2
import pytest
import json
import sys
import stix2.exceptions


def test_args_response_requested():
    valid = ["none", "ack", "status", "complete"]
    for v in valid:
        a = openc2.v10.Args(response_requested=v)
        print(a)
        ser_a = json.loads(a.serialize())
        b = openc2.v10.Args(**ser_a)
        assert a == b

    with pytest.raises(stix2.exceptions.InvalidValueError):
        openc2.v10.Args(response_requested="bad")


def test_args_start_time():
    # Value is the number of milliseconds since 00:00:00 UTC, 1 January 1970

    for time in range(0, 15):
        a = openc2.v10.Args(start_time=time)
        assert a.start_time == time

    a = openc2.v10.Args(start_time=sys.maxsize)
    assert a.start_time == sys.maxsize

    invalid = ["a", "invalid", -1]

    for item in invalid:
        with pytest.raises(stix2.exceptions.InvalidValueError):
            openc2.v10.Args(start_time=item)

    # xxx: floats are currently valid and passing


def test_args_stop_time():
    # Value is the number of milliseconds since 00:00:00 UTC, 1 January 1970

    for time in range(0, 15):
        a = openc2.v10.Args(stop_time=time)
        assert a.stop_time == time

    a = openc2.v10.Args(stop_time=sys.maxsize)
    assert a.stop_time == sys.maxsize

    invalid = ["a", "invalid", -1]

    for item in invalid:
        with pytest.raises(stix2.exceptions.InvalidValueError):
            openc2.v10.Args(stop_time=item)

    # xxx: floats etc is currently valid and passing


def test_args_duration():
    # Value is the number of milliseconds since 00:00:00 UTC, 1 January 1970

    for time in range(0, 15):
        a = openc2.v10.Args(duration=time)
        assert a.duration == time

    a = openc2.v10.Args(duration=sys.maxsize)
    assert a.duration == sys.maxsize

    invalid = ["a", "invalid", -1]

    for item in invalid:
        with pytest.raises(stix2.exceptions.InvalidValueError):
            openc2.v10.Args(duration=item)

    # xxx: floats etc is currently valid and passing


def test_args_combination():
    # Only two of the three are allowed on any given Command and the third is derived from the equation stop_time = start_time + duration.
    with pytest.raises(stix2.exceptions.PropertyPresenceError):
        openc2.v10.Args(start_time=1, stop_time=1, duration=1)

    with pytest.raises(stix2.exceptions.InvalidValueError):
        openc2.v10.Args(start_time=1, stop_time=0)

def test_args_allow_custom():
    a = openc2.v10.Args(duration=sys.maxsize)
    foo = openc2.v10.Args(allow_custom=True, what="who", item=a)

    with pytest.raises(AttributeError):
        openc2.core.parse_args(foo.serialize())

    with pytest.raises(stix2.exceptions.CustomContentError):
        bar = openc2.core.parse_args(json.loads(foo.serialize()))

    bar = openc2.core.parse_args(json.loads(foo.serialize()), allow_custom=True)
    assert foo == bar

def test_args_custom():
    @openc2.CustomArgs("custom-args", [("id", stix2.properties.StringProperty())])
    class MyCustomArgs(object):
        pass

    foo = MyCustomArgs(id="value")
    assert foo.id == "value"

    bar = openc2.core.parse_args(json.loads(foo.serialize()), allow_custom=True)
    assert bar == foo

    args = {"custom-args": json.loads(foo.serialize())}

    bar = openc2.core.parse_args(args, allow_custom=True)
    assert bar['custom-args'] == foo

    args = {"bad-custom-args": json.loads(foo.serialize())}

    with pytest.raises(stix2.exceptions.CustomContentError):
        bar = openc2.core.parse_args(args)

    args = {"custom-args": MyCustomArgs(id="value")}
    bar = openc2.core.parse_args(args, allow_custom=True)

    args = {"custom-args": openc2.Args(id="value", allow_custom=True)}
    with pytest.raises(ValueError):
        openc2.core.parse_args(args)

