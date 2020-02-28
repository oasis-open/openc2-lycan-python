from openc2 import parse
from openc2 import (
    parse,
    Command,
    Args,
    Payload,
    Device,
    DomainName,
    EmailAddress,
    IPv4Connection,
    Response,
    File,
    Artifact,
    Process,
    Features,
    InternationalizedDomainName,
    InternationalizedEmailAddress,
    IPv4Address,
    IPv6Address,
    IPv6Connection,
    MACAddress,
    IRI,
    Properties,
    URI,
)

# Artifact
hashes = {
    "sha1": "1234567890ABCDEF1234567890ABCDEF12345678",
    "sha256": "1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABDEF1",
    "md5": "1234567890ABCDEF1234567890ABCDEF",
}
p = Payload(url="www.testurl.com")
a = Artifact(payload=p, hashes=hashes, mime_type="My MIME Type")
cmd = Command(action="contain", target=a)
with open("Artifact.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Artifact with args
cmd = Command(
    action="start",
    target=a,
    args=Args(
        start_time=1568209029693,
        stop_time=1568209059693,
        response_requested="complete",
    ),
)
with open("Artifact2.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Artifact with args
cmd = Command(
    action="start",
    target=a,
    args=Args(duration=30000, start_time=1568209029693, response_requested="complete",),
)
with open("Artifact3.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Artifact with bin
cmd = Command(
    action="stop",
    target=Artifact(
        payload=Payload(bin="YmluIGRhdGE="), hashes=hashes, mime_type="My MIME Type"
    ),
)
with open("Artifact4.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Artifact (update)
cmd = Command(action="update", target=a)
with open("Artifact5.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Device
cmd = Command(
    action="allow",
    target=Device(
        hostname="device hostname",
        idn_hostname="device idn hostname",
        device_id="Device id",
    ),
)
with open("Device.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Domain Name
cmd = Command(action="cancel", target=DomainName(domain_name="Domain name"))
with open("DomainName.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Email Address
cmd = Command(action="copy", target=EmailAddress(email_addr="Email address"))
with open("EmailAddress.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Features
cmd = Command(
    action="create",
    target=Features(features=["versions", "profiles", "pairs", "rate_limit"]),
)
with open("Features.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# File
f = File(name="File name", path="File path", hashes=hashes)
cmd = Command(action="delete", target=f)
with open("File.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# IdnDomainName
cmd = Command(
    action="deny", target=InternationalizedDomainName(idn_domain_name="IDN Domain name")
)
with open("IdnDomainName.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# IdnEmailAddress
cmd = Command(
    action="detonate",
    target=InternationalizedEmailAddress(idn_email_addr="IDN Email address"),
)
with open("IdnEmailAddress.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Ipv4Connection
cmd = Command(
    action="investigate",
    target=IPv4Connection(
        src_addr="10.0.0.0/24",
        src_port=8443,
        dst_addr="10.0.0.0/24",
        dst_port=9443,
        protocol="tcp",
    ),
)
with open("Ipv4Connection.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Ipv4Net
cmd = Command(action="locate", target=IPv4Address(ipv4_net="10.0.0.0/24"))
with open("Ipv4Net.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Ipv6Connection
cmd = Command(
    action="query",
    target=IPv6Connection(
        src_addr="AE:00:E4:F1:04:65/24",
        src_port=8443,
        dst_addr="AE:00:E4:F1:04:65/24",
        dst_port=9443,
        protocol="tcp",
    ),
)
with open("Ipv6Connection.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Ipv6Net
cmd = Command(action="locate", target=IPv6Address(ipv6_net="AE:00:E4:F1:04:65/24"))
with open("Ipv6Net.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Iri
cmd = Command(action="remediate", target=IRI(iri="My IRI identifier"))
with open("Iri.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# MacAddress
cmd = Command(
    action="restart", target=MACAddress(mac_addr="VGhpcyBpcyBteSBtYWMgYWRkcmVzcw==")
)
with open("MacAddress.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Parent
parent = Process(pid=43521, name="Process parent name", cwd="Process parent CWD")
cmd = Command(
    action="restore",
    target=Process(
        pid=12354,
        name="Process name",
        cwd="Process CWD",
        executable=f,
        parent=parent,
        command_line="Process command line statement",
    ),
)
with open("Process.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Properties
cmd = Command(action="set", target=URI(uri="www.myuri.com"))
with open("URI.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")

# Properties
cmd = Command(
    action="scan", target=Properties(properties=["Tag1", "Tag2", "Tag3", "Tag4"])
)
with open("Properties.json", "w") as OUT:
    OUT.write(cmd.serialize(pretty=True) + "\n")
