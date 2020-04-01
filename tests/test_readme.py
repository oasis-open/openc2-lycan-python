def test_readme():
    import openc2

    # encode
    cmd = openc2.v10.Command(
        action="deny",
        target=openc2.v10.IPv4Address(ipv4_net="1.2.3.4"),
        args=openc2.v10.Args(response_requested="complete"),
    )
    msg = cmd.serialize()

    # decode
    cmd = openc2.parse(msg)
    if cmd.action == "deny" and cmd.target.type == "ipv4_net":

        if cmd.args.response_requested == "complete":
            resp = openc2.v10.Response(status=200)
            msg = resp.serialize()

    # custom actuator
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
