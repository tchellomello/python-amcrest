"""Test utils.py functions."""
from unittest import TestCase

from amcrest.utils import clean_url, percent, str2bool, to_unit


class TestUtils(TestCase):
    """Tests for utils.py."""

    def test_clean_url(self):
        """Test return code from utils.clean_url."""
        self.assertEqual('www.foo.bar', clean_url('http://www.foo.bar/'))
        self.assertEqual('www.foo.bar', clean_url('https://www.foo.bar'))

    def test_precision(self):
        """Test return code from utils.precision."""
        self.assertEqual("10.0", percent(10, 100))
        self.assertRaises(TypeError, percent, 'a', 100)

    def test_str2bool(self):
        """Test return code from utils.str2bool."""
        self.assertTrue(str2bool('y'))
        self.assertTrue(str2bool('Y'))
        self.assertTrue(str2bool('yes'))
        self.assertTrue(str2bool(1))
        self.assertFalse(str2bool('n'))
        self.assertFalse(str2bool('N'))
        self.assertFalse(str2bool('no'))
        self.assertFalse(str2bool(0))
        self.assertTrue(str2bool(u'Y'))
        self.assertRaises(ValueError, str2bool, 'amcrest')

    def test_to_unit(self):
        """Test return code from utils.to_unit."""
        self.assertEqual("1024.0", to_unit(1024, unit='B')[0])
        self.assertEqual("8192.0", to_unit(8589934592, unit='MB')[0])
        self.assertEqual("1024.0", to_unit(1099511627776, unit='GB')[0])
        self.assertNotEqual("117.73", to_unit('123000300', unit='MB')[0])
