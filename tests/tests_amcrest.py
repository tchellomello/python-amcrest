"""Tests for Amcrest module."""
import unittest


class TestAmcrest(unittest.TestCase):
    """Tests for Amcrest basic"""

    def test_call(self):
        """Simple test call"""
        from amcrest import AmcrestCamera
        amcrest = AmcrestCamera('192.168.0.1', 80, 'admin', 'password')
