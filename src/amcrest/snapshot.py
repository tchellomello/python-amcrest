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
import logging
from urllib3.exceptions import HTTPError

from .exceptions import CommError

_LOGGER = logging.getLogger(__name__)


class Snapshot(object):
    def __get_config(self, config_name):
        ret = self.command(
            'configManager.cgi?action=getConfig&name={0}'.format(config_name)
        )
        return ret.content.decode('utf-8')

    @property
    def snapshot_config(self):
        return self.__get_config('Snap')

    def snapshot(self, channel=None, path_file=None, timeout=None,
                 stream=True):
        """
        Args:

            channel:
                Video input channel number

                If no channel param is used, don't send channel parameter
                so camera will use its default channel

            path_file:
                If path_file is provided, save the snapshot
                in the path

        Return:
            raw from http request if stream is True
            response content if stream is False
        """
        cmd = "snapshot.cgi"
        if channel is not None:
            cmd += "?channel={}".format(channel)
        ret = self.command(cmd, timeout_cmd=timeout, stream=stream)

        if path_file:
            with open(path_file, 'wb') as out_file:
                if stream:
                    try:
                        shutil.copyfileobj(ret.raw, out_file)
                    except HTTPError as error:
                        _LOGGER.debug(
                            "%s Snapshot to file failed due to error: %s",
                            self, repr(error))
                        raise CommError(error)
                else:
                    out_file.write(ret.content)

        return ret.raw if stream else ret.content
