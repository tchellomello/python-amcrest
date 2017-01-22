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

from distutils.util import strtobool

PRECISION = 2


class Utils:

    def str2bool(self, value):
        """
        Args:
            value - text to be converted to boolean
             True values: y, yes, true, t, on, 1
             False values: n, no, false, off, 0
        """
        return bool(strtobool(value))

    def to_unit(self, value, unit='B'):
        """Convert bytes to give unit."""
        BYTE_SIZES = ['B', 'KB', 'MB', 'GB', 'TB']

        if not isinstance(value, (int, float)):
            value = float(value)

        if unit in BYTE_SIZES:
            result = value / 1024**BYTE_SIZES.index(unit)
            return (float('{:.{prec}f}'.format(result, prec=PRECISION)), unit)

    def percent(self, part, whole):
        """Convert data to percent"""
        result = 100 * float(part)/float(whole)
        return float('{:.{prec}f}'.format(result, prec=PRECISION))
