"""Amcrest NAS."""
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


class Nas(object):
    """Amcrest methods to handle NAS."""

    @property
    def nas_information(self):
        """Return NAS information."""
        ret = self.command(
            'configManager.cgi?action=getConfig&name=NAS'
        )
        return ret.content.decode('utf-8')
