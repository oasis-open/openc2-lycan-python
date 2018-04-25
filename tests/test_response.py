import unittest
from lycan.message import OpenC2Response

class TestOpenC2Response(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_init_fail(self):
        self.assertRaises(TypeError, OpenC2Response, 'firewall')
    def test_init(self):
        x = OpenC2Response('firewall', 'completed', 'passed', 1, 'foo')
        self.assertEqual(x.source, 'firewall')
