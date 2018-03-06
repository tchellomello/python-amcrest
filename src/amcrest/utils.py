# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# vim:sw=4:ts=4:et

import re

# pylint: disable=no-name-in-module
from distutils import util

PRECISION = 2


def clean_url(url):
    host = re.sub(r'^http[s]?://', '', url, flags=re.IGNORECASE)
    host = re.sub(r'/$', '', host)
    return host


def pretty(value, delimiter='='):
    """Format string key=value."""
    try:
        return value.split(delimiter)[1]
    except AttributeError:
        pass


def percent(part, whole):
    """Convert data to percent"""
    result = 100 * float(part) / float(whole)
    return float('{:.{prec}f}'.format(result, prec=PRECISION))


def str2bool(value):
    """
    Args:
        value - text to be converted to boolean
         True values: y, yes, true, t, on, 1
         False values: n, no, false, off, 0
    """
    try:
        if isinstance(value, (str, unicode)):
            return bool(util.strtobool(value))
    except NameError:  # python 3
        if isinstance(value, str):
            return bool(util.strtobool(value))
    return bool(value)


def to_unit(value, unit='B'):
    """Convert bytes to give unit."""
    byte_array = ['B', 'KB', 'MB', 'GB', 'TB']

    if not isinstance(value, (int, float)):
        value = float(value)

    if unit in byte_array:
        result = value / 1024**byte_array.index(unit)
        return (float('{:.{prec}f}'.format(result, prec=PRECISION)), unit)

    return value
