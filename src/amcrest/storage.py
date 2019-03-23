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
from .exceptions import AmcrestError
from .utils import to_unit, percent, pretty


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

    def _extract_storage_value(self, param, unit):
        try:
            return to_unit(
                pretty([part for part in self.storage_device_info.split()
                        if '.{}='.format(param) in part][0]),
                unit)
        except (AmcrestError, AttributeError, IndexError):
            return 'unknown', 'GB'

    @property
    def storage_used(self):
        return self._extract_storage_value('UsedBytes', 'GB')

    @property
    def storage_total(self):
        return self._extract_storage_value('TotalBytes', 'GB')

    @property
    def storage_used_percent(self):
        try:
            return percent(self.storage_used[0], self.storage_total[0])
        except (ValueError, ZeroDivisionError):
            return 'unknown'
