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


class Record:

    @property
    def record_capability(self):
        ret = self.command(
            'recordManager.cgi?action=getCaps'
        )
        return ret.content.decode('utf-8')

    @property
    def record_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=Record'
        )
        return ret.content.decode('utf-8')

    @property
    def media_global_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=MediaGlobal'
        )
        return ret.content.decode('utf-8')

    @property
    def record_mode(self):
        status_code = {0: 'Automatic',
                       1: 'Manual',
                       2: 'Stop',
                       None: 'Unknown'}

        ret = self.command(
            'configManager.cgi?action=getConfig&name=RecordMode'
        )

        try:
            status = int([s for s in ret.content.decode(
                'utf-8').split() if 'Mode=' in s][0].split('=')[-1])
        except:
            status = None

        return status_code[status]
