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

from .system import System
from .network import Network
from .motion_detection import MotionDetection
from .snapshot import Snapshot


class Http(System, Network, MotionDetection, Snapshot):
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

    def command(self, cmd):
        try:
            url = self.__base_url(cmd)
            resp = requests.get(url, auth=self._token, stream=True)
            resp.raise_for_status()
        except:
            raise

        return resp
