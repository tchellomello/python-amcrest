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
import re

from requests.adapters import HTTPAdapter

from .audio import Audio
from .event import Event
from .log import Log
from .motion_detection import MotionDetection
from .nas import Nas
from .network import Network
from .ptz import Ptz
from .record import Record
from .snapshot import Snapshot
from .special import Special
from .storage import Storage
from .system import System
from .user_management import UserManagement
from .utils import Utils
from .video import Video

from .config import TIMEOUT_HTTP_PROTOCOL, MAX_RETRY_HTTP_CONNECTION


class Http(System, Network, MotionDetection, Snapshot,
           UserManagement, Event, Audio, Record, Video,
           Log, Ptz, Special, Storage, Utils, Nas):

    def __init__(self, host, port, user,
                 password, verbose=True, protocol='http',
                 retries_connection=None, timeout_protocol=None):
        self._host = self.__clean_url(host)
        self._port = port
        self._user = user
        self._password = password
        self._verbose = verbose
        self._protocol = protocol
        self._token = requests.auth.HTTPBasicAuth(self._user, self._password)
        self._base_url = self.__base_url()

        if timeout_protocol is None:
            self._timeout_protocol = TIMEOUT_HTTP_PROTOCOL
        else:
            self._timeout_protocol = timeout_protocol

        if retries_connection is None:
            self._retries_conn = MAX_RETRY_HTTP_CONNECTION
        else:
            self._retries_conn = retries_connection

    # Base methods
    def __clean_url(self, url):
        host = re.sub(r'^http[s]?://', '', url, flags=re.IGNORECASE)
        host = re.sub(r'/$', '', host)
        return host

    def __base_url(self, param=""):
        return '%s://%s:%s/cgi-bin/%s' % (self._protocol, self._host,
                                          str(self._port), param)

    def command(self, cmd, retries=None, timeout_cmd=None):
        """
        Args:
            cmd - command to execute via http
            timeout_cmd - timeout, default 3sec
            retries - maximum number of retries each connection should attempt
        """
        if timeout_cmd is not None:
            self._timeout_protocol = timeout_cmd

        if retries is not None:
            self._retries_conn = retries

        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=self._retries_conn))
        s.mount('https://', HTTPAdapter(max_retries=self._retries_conn))

        url = self.__base_url(cmd)
        try:
            resp = s.get(
                url,
                auth=self._token,
                stream=True,
                timeout=self._timeout_protocol,
            )
            resp.raise_for_status()
        except:
            raise
        return resp
