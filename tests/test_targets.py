import openc2
import pytest

import stix2.exceptions


def test_ipv4_address_example():
    ip4 = openc2.v10.IPv4Address(
        ipv4_net="198.51.100.3")
    
    assert ip4.ipv4_net == "198.51.100.3"

    ip4 = openc2.v10.IPv4Address(
        ipv4_net="198.51.100.0/24")

    assert ip4.ipv4_net == "198.51.100.0/24"

    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        ip4 = openc2.v10.IPv4Address()
    
    assert excinfo.value.cls == openc2.v10.IPv4Address

