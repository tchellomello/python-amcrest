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
import shutil


class Snapshot(object):
    def __get_config(self, config_name):
        ret = self.command(
            'configManager.cgi?action=getConfig&name={0}'.format(config_name)
        )
        return ret.content.decode('utf-8')

    @property
    def snapshot_config(self):
        return self.__get_config('Snap')

    def snapshot(self, channel=0, path_file=None, timeout=None):
        """
        Args:

            channel:
                Values according with Amcrest API:
                0 - regular snapshot
                1 - motion detection snapshot
                2 - alarm snapshot

                If no channel param is used, default is 0

            path_file:
                If path_file is provided, save the snapshot
                in the path

        Return:
            raw from http request
        """
        ret = self.command(
            "snapshot.cgi?channel={0}".format(channel),
            timeout_cmd=timeout
        )

        if path_file:
            with open(path_file, 'wb') as out_file:
                shutil.copyfileobj(ret.raw, out_file)

        return ret.raw
