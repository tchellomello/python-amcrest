"""
amcrest.exceptions

This module contains the set of amcrest's exceptions.
"""


class AmcrestError(Exception):
    """General Amcrest error occurred."""


class CommError(AmcrestError):
    """A communication error occurred."""


class LoginError(AmcrestError):
    """A login error occurred."""
