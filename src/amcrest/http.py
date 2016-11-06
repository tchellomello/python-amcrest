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
import requests

from .audio import Audio
from .system import System
from .network import Network
from .motion_detection import MotionDetection
from .snapshot import Snapshot
from .user_management import UserManagement
from .event import Event
from .record import Record
from .video import Video
from .log import Log
from .ptz import Ptz
from .special import Special


class Http(System, Network, MotionDetection, Snapshot,
           UserManagement, Event, Audio, Record, Video,
           Log, Ptz, Special):

    def __init__(self, host, port, user,
                 password, verbose=True, protocol='http'):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._verbose = verbose
        self._protocol = protocol
        self._token = requests.auth.HTTPBasicAuth(self._user, self._password)

    # Base methods
    def __base_url(self, param=""):
        return '%s://%s:%s/cgi-bin/%s' % (self._protocol, self._host,
                                          str(self._port), param)

    def command(self, cmd, timeout_cmd=3):
        """
        Args:
            cmd - command to execute via http
            timeout_cmd - timeout, default 3sec
        """
        try:
            url = self.__base_url(cmd)
            resp = requests.get(
                url,
                auth=self._token,
                stream=True,
                timeout=timeout_cmd,
            )
            resp.raise_for_status()
        except:
            raise

        return resp
