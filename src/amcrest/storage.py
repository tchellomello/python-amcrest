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

from .exceptions import AmcrestError
from .utils import to_unit, percent

_USED = '.UsedBytes'
_TOTAL = '.TotalBytes'


def _express_as(value, unit):
    try:
        return to_unit(value, unit)
    except (TypeError, ValueError):
        return 'unknown', unit


class Storage(object):

    @property
    def storage_device_info(self):
        ret = self.command(
            'storageDevice.cgi?action=getDeviceAllInfo'
        )
        return ret.content.decode('utf-8')

    @property
    def storage_device_names(self):
        ret = self.command(
            'storageDevice.cgi?action=factory.getCollect'
        )
        return ret.content.decode('utf-8')

    def _get_storage_values(self, *params):
        info = self.storage_device_info
        ret = []
        for param in params:
            try:
                ret.append(
                    re.search('.{}=([0-9.]+)'.format(param), info).group(1))
            except AttributeError:
                ret.append(None)
        if len(params) == 1:
            return ret[0]
        return ret

    @property
    def storage_used(self):
        return _express_as(self._get_storage_values(_USED), 'GB')

    @property
    def storage_total(self):
        return _express_as(self._get_storage_values(_TOTAL), 'GB')

    @property
    def storage_used_percent(self):
        used, total = self._get_storage_values(_USED, _TOTAL)
        try:
            return percent(used, total)
        except (TypeError, ValueError, ZeroDivisionError):
            return 'unknown'

    @property
    def storage_all(self):
        used, total = self._get_storage_values(_USED, _TOTAL)
        try:
            used_percent = percent(used, total)
        except (TypeError, ValueError, ZeroDivisionError):
            used_percent = 'unknown'
        return {
            'used_percent': used_percent,
            'used': _express_as(used, 'GB'),
            'total': _express_as(total, 'GB')}
