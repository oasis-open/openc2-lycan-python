import openc2
import pytest
import json
import sys


def test_cmd_create():
    with pytest.raises(openc2.exceptions.MissingPropertiesError):
        openc2.v10.Command()

    with pytest.raises(openc2.exceptions.MissingPropertiesError):
        openc2.v10.Command(action="query")

    with pytest.raises(openc2.exceptions.MissingPropertiesError):
        openc2.v10.Command(target=openc2.v10.Features())

    foo = openc2.v10.Command(action="query", target=openc2.v10.Features())
    assert foo
    assert foo.action == "query"
    assert foo.target.features == []
    assert '"action": "query"' in foo.serialize()
    assert '"target": {"features": []}' in foo.serialize()

    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert bar == foo

    bar = openc2.parse(foo.serialize())
    assert foo == bar

    d = json.loads(foo.serialize())
    foo = openc2.utils.dict_to_openc2(d)
    d["invalid"] = {"bad": "value"}
    with pytest.raises(openc2.exceptions.ExtraPropertiesError):
        openc2.utils.dict_to_openc2(d)

    with pytest.raises(openc2.exceptions.InvalidValueError):
        openc2.v10.Command(action="invalid", target=openc2.v10.Features())

    with pytest.raises(openc2.exceptions.InvalidValueError):
        openc2.v10.Command(action="query", target=openc2.v10.Args())


def test_cmd_custom_actuator():
    @openc2.v10.CustomActuator(
        "x-acme-widget",
        [
            ("name", openc2.properties.StringProperty(required=True)),
            ("version", openc2.properties.FloatProperty()),
        ],
    )
    class AcmeWidgetActuator(object):
        def __init__(self, version=None, **kwargs):
            if version and version < 1.0:
                raise ValueError("'%f' is not a supported version." % version)

    widget = AcmeWidgetActuator(name="foo", version=1.1)
    foo = openc2.v10.Command(
        action="query", target=openc2.v10.Features(), actuator=widget
    )
    assert foo
    assert foo.action == "query"
    assert foo.actuator.name == "foo"
    assert foo.actuator.version == 1.1

    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert bar == foo

    bar = openc2.parse(foo.serialize())
    assert foo == bar


def test_cmd_slpf_actuator():
    widget = openc2.v10.SLPFActuator(hostname="localhost")
    foo = openc2.v10.Command(
        action="query", target=openc2.v10.Features(), actuator=widget
    )
    assert foo
    assert foo.action == "query"
    assert foo.actuator.hostname == "localhost"
    assert '"action": "query"' in foo.serialize()
    assert '"target": {"features": []}' in foo.serialize()
    assert '"actuator": {"slpf": {"hostname": "localhost"}}' in foo.serialize()

    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert bar == foo

    bar = openc2.parse(foo.serialize())
    assert foo == bar


def test_cmd_custom():
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

    @openc2.v10.CustomTarget("x-thing:id", [("id", CustomTargetProperty())])
    class CustomTarget(object):
        pass

    @openc2.v10.CustomArgs(
        "whatever-who-cares", [("custom_args", CustomTargetProperty())]
    )
    class CustomArgs(object):
        pass

    @openc2.v10.CustomActuator(
        "x-acme-widget",
        [
            ("name", openc2.properties.StringProperty(required=True)),
            ("version", CustomTargetProperty()),
        ],
    )
    class AcmeWidgetActuator(object):
        pass

    tp = CustomTargetProperty(name="target")
    t = CustomTarget(id=tp)
    args = CustomArgs(custom_args=CustomTargetProperty(name="args"))
    act = AcmeWidgetActuator(
        name="hello", version=CustomTargetProperty(name="actuator")
    )
    cmd = openc2.v10.Command(action="query", target=t, args=args, actuator=act)

    bar = openc2.parse(cmd.serialize())
    assert cmd == bar
    bar = openc2.parse(json.loads(cmd.serialize()))
    assert cmd == bar

    bar = openc2.v10.Command(**json.loads(cmd.serialize()))
    assert cmd == bar


def test_cmd_device():
    gen = """{
    "action": "allow",
    "target": {
        "device": {
            "hostname": "device hostname",
            "idn_hostname": "device idn hostname",
            "device_id": "Device id"
        }
    }
}
"""
    foo = openc2.parse(gen)
    assert foo.action == "allow"
    assert isinstance(foo.target, openc2.v10.Device)
    assert foo.target.hostname == "device hostname"
    assert foo.target.idn_hostname == "device idn hostname"
    assert foo.target.device_id == "Device id"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_domain():
    gen = """{
    "action": "cancel",
    "target": {
        "domain_name": "Domain name"
    }
}"""
    foo = openc2.parse(gen)
    assert foo.action == "cancel"
    assert isinstance(foo.target, openc2.v10.DomainName)
    assert foo.target.domain_name == "Domain name"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_email():
    gen = """{
    "action": "copy",
    "target": {
        "email_addr": "Email address"
    }
}"""
    foo = openc2.parse(gen)
    assert foo.action == "copy"
    assert isinstance(foo.target, openc2.v10.EmailAddress)
    assert foo.target.email_addr == "Email address"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_features():
    gen = """{
    "action": "create",
    "target": {
        "features": [
            "versions",
            "profiles",
            "pairs",
            "rate_limit"
        ]
    }
}"""
    foo = openc2.parse(gen)
    assert foo.action == "create"
    assert isinstance(foo.target, openc2.v10.Features)
    assert foo.target.features == ["versions", "profiles", "pairs", "rate_limit"]

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_file():
    gen = """{
    "action": "delete",
    "target": {
        "file": {
            "name": "File name",
            "path": "File path",
            "hashes": {
                "sha1": "1234567890ABCDEF1234567890ABCDEF12345678",
                "sha256": "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABDEF1",
                "md5": "1234567890ABCDEF1234567890ABCDEF"
            }
        }
    }
}"""
    foo = openc2.parse(gen)
    assert foo.action == "delete"
    assert isinstance(foo.target, openc2.v10.File)
    assert foo.target.name == "File name"
    assert foo.target.path == "File path"
    assert foo.target.hashes

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_idn():
    gen = """{
    "action": "deny",
    "target": {
        "idn_domain_name": "IDN Domain name"
    }
}"""
    foo = openc2.parse(gen)
    assert foo.action == "deny"
    assert isinstance(foo.target, openc2.v10.InternationalizedDomainName)
    assert foo.target.idn_domain_name == "IDN Domain name"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar

    gen = """{
    "action": "detonate",
    "target": {
        "idn_email_addr": "IDN Email address"
    }
}"""
    foo = openc2.parse(gen)
    assert foo.action == "detonate"
    assert isinstance(foo.target, openc2.v10.InternationalizedEmailAddress)
    assert foo.target.idn_email_addr == "IDN Email address"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_ip():
    gen = """{
    "action": "investigate",
    "target": {
        "ipv4_connection": {
            "src_addr": "10.0.0.0/24",
            "src_port": 8443,
            "dst_addr": "10.0.0.0/24",
            "dst_port": 9443,
            "protocol": "tcp"
        }
    }
}
"""
    foo = openc2.parse(gen)
    assert foo.action == "investigate"
    assert isinstance(foo.target, openc2.v10.IPv4Connection)
    assert foo.target.src_addr == "10.0.0.0/24"
    assert foo.target.src_port == 8443
    assert foo.target.dst_addr == "10.0.0.0/24"
    assert foo.target.dst_port == 9443
    assert foo.target.protocol == "tcp"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar

    gen = """{
    "action": "locate",
    "target": {
        "ipv4_net": "10.0.0.0/24"
    }
}

"""
    foo = openc2.parse(gen)
    assert foo.action == "locate"
    assert isinstance(foo.target, openc2.v10.IPv4Address)
    assert foo.target.ipv4_net == "10.0.0.0/24"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar

    gen = """{
    "action": "query",
    "target": {
        "ipv6_connection": {
            "src_addr": "AE:00:E4:F1:04:65/24",
            "src_port": 8443,
            "dst_addr": "AE:00:E4:F1:04:65/24",
            "dst_port": 9443,
            "protocol": "tcp"
        }
    }
}
"""
    foo = openc2.parse(gen)
    assert foo.action == "query"
    assert isinstance(foo.target, openc2.v10.IPv6Connection)
    assert foo.target.src_addr == "AE:00:E4:F1:04:65/24"
    assert foo.target.src_port == 8443
    assert foo.target.dst_addr == "AE:00:E4:F1:04:65/24"
    assert foo.target.dst_port == 9443
    assert foo.target.protocol == "tcp"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar

    gen = """{
    "action": "locate",
    "target": {
        "ipv6_net": "AE:00:E4:F1:04:65/24"
    }
}
"""
    foo = openc2.parse(gen)
    assert foo.action == "locate"
    assert isinstance(foo.target, openc2.v10.IPv6Address)
    assert foo.target.ipv6_net == "AE:00:E4:F1:04:65/24"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_iri():
    gen = """{
    "action": "remediate",
    "target": {
        "iri": "My IRI identifier"
    }
}
"""
    foo = openc2.parse(gen)
    assert foo.action == "remediate"
    assert isinstance(foo.target, openc2.v10.IRI)
    assert foo.target.iri == "My IRI identifier"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_mac():
    gen = """{
    "action": "restart",
    "target": {
        "mac_addr": "VGhpcyBpcyBteSBtYWMgYWRkcmVzcw=="
    }
}
"""
    foo = openc2.parse(gen)
    assert foo.action == "restart"
    assert isinstance(foo.target, openc2.v10.MACAddress)
    assert foo.target.mac_addr == "VGhpcyBpcyBteSBtYWMgYWRkcmVzcw=="

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_process():
    gen = """{
    "action": "restore",
    "target": {
        "process": {
            "pid": 12354,
            "name": "Process name",
            "cwd": "Process CWD",
            "executable": {
                "name": "File name",
                "path": "File path",
                "hashes": {
                    "sha1": "1234567890ABCDEF1234567890ABCDEF12345678",
                    "sha256": "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABDEF1",
                    "md5": "1234567890ABCDEF1234567890ABCDEF"
                }
            },
            "parent": {
                "pid": 43521,
                "name": "Process parent name",
                "cwd": "Process parent CWD"
            },
            "command_line": "Process command line statement"
        }
    }
}
"""
    foo = openc2.parse(gen)
    assert foo.action == "restore"
    assert isinstance(foo.target, openc2.v10.Process)
    assert foo.target.pid == 12354
    assert foo.target.name == "Process name"
    assert foo.target.cwd == "Process CWD"
    assert foo.target.executable
    assert foo.target.parent
    assert foo.target.command_line == "Process command line statement"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_properties():
    gen = """{
    "action": "scan",
    "target": {
        "properties": [
            "Tag1",
            "Tag2",
            "Tag3",
            "Tag4"
        ]
    }
}
"""
    foo = openc2.parse(gen)
    assert foo.action == "scan"
    assert isinstance(foo.target, openc2.v10.Properties)
    assert foo.target.properties == ["Tag1", "Tag2", "Tag3", "Tag4"]

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_uri():
    gen = """{
    "action": "set",
    "target": {
        "uri": "www.myuri.com"
    }
}"""
    foo = openc2.parse(gen)
    assert foo.action == "set"
    assert isinstance(foo.target, openc2.v10.URI)
    assert foo.target.uri == "www.myuri.com"

    bar = openc2.parse(foo.serialize())
    assert foo == bar
    bar = openc2.parse(json.loads(foo.serialize()))
    assert foo == bar
    bar = openc2.v10.Command(**json.loads(foo.serialize()))
    assert foo == bar


def test_cmd_generated():
    generated = []
    generated.append(
        """{
    "action": "contain",
    "target": {
        "artifact": {
            "payload": {
                "url": "www.testurl.com"
            },
            "hashes": {
                "sha1": "1234567890ABCDEF1234567890ABCDEF12345678",
                "sha256": "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABDEF1",
                "md5": "1234567890ABCDEF1234567890ABCDEF"
            },
            "mime_type": "My MIME Type"
        }
    }
}
"""
    )
    generated.append(
        """{
    "action": "start",
    "target": {
        "artifact": {
            "payload": {
                "url": "www.testurl.com"
            },
            "hashes": {
                "sha1": "1234567890ABCDEF1234567890ABCDEF12345678",
                "sha256": "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABDEF1",
                "md5": "1234567890ABCDEF1234567890ABCDEF"
            },
            "mime_type": "My MIME Type"
        }
    },
    "args": {
        "start_time": 1568209029693,
        "stop_time": 1568209059693,
        "response_requested": "complete"
    }
}
"""
    )
    generated.append(
        """{
    "action": "start",
    "target": {
        "artifact": {
            "payload": {
                "url": "www.testurl.com"
            },
            "hashes": {
                "sha1": "1234567890ABCDEF1234567890ABCDEF12345678",
                "sha256": "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABDEF1",
                "md5": "1234567890ABCDEF1234567890ABCDEF"
            },
            "mime_type": "My MIME Type"
        }
    },
    "args": {
        "duration": 30000,
        "start_time": 1568209029693,
        "response_requested": "complete"
    }
}
"""
    )
    generated.append(
        """{
    "action": "stop",
    "target": {
        "artifact": {
            "payload": {
                "bin": "YmluIGRhdGE="
            },
            "hashes": {
                "sha1": "1234567890ABCDEF1234567890ABCDEF12345678",
                "sha256": "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABDEF1",
                "md5": "1234567890ABCDEF1234567890ABCDEF"
            },
            "mime_type": "My MIME Type"
        }
    }
}
"""
    )
    generated.append(
        """{
    "action": "update",
    "target": {
        "artifact": {
            "payload": {
                "url": "www.testurl.com"
            },
            "hashes": {
                "sha1": "1234567890ABCDEF1234567890ABCDEF12345678",
                "sha256": "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABDEF1",
                "md5": "1234567890ABCDEF1234567890ABCDEF"
            },
            "mime_type": "My MIME Type"
        }
    }
}
"""
    )
    for gen in generated:
        foo = openc2.parse(gen)

        bar = openc2.parse(foo.serialize())
        assert foo == bar
        bar = openc2.parse(json.loads(foo.serialize()))
        assert foo == bar
        bar = openc2.v10.Command(**json.loads(foo.serialize()))
        assert foo == bar
