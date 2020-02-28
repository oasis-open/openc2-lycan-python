import openc2
import stix2
import json
import collections


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


@openc2.CustomTarget("x-thing:id", [("id", CustomTargetProperty())])
class CustomTarget(object):
    pass


@openc2.CustomArgs("whatever-who-cares", [("custom_args", CustomTargetProperty())])
class CustomArgs(object):
    pass


@openc2.CustomActuator(
    "x-acme-widget",
    [
        ("name", stix2.properties.StringProperty(required=True)),
        ("version", CustomTargetProperty()),
    ],
)
class AcmeWidgetActuator(object):
    pass


def main():
    print("=== Creating Command")
    tp = CustomTargetProperty(name="target")
    print("target property", tp)
    t = CustomTarget(id=tp)
    print("target", t)
    args = CustomArgs(custom_args=CustomTargetProperty(name="args"))
    print("args", args)
    act = AcmeWidgetActuator(
        name="hello", version=CustomTargetProperty(name="actuator")
    )
    print("actuator", act)
    cmd = openc2.Command(action="query", target=t, args=args, actuator=act)

    d = json.loads(cmd.serialize())
    print("=== COMMAND START ===")
    print(d)
    print("=== COMMAND END ===")
    print()

    print("=== Parsing command back to command ===")
    cmd2 = openc2.Command(**d)
    print("=== COMMAND START ===")
    print(cmd2)
    print("=== COMMAND END ===")

    assert cmd == cmd2


if __name__ == "__main__":
    main()
