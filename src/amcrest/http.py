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
import logging

import requests
from requests.adapters import HTTPAdapter

from .exceptions import CommError, LoginError
from .utils import clean_url, pretty

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
from .video import Video

from .config import TIMEOUT_HTTP_PROTOCOL, MAX_RETRY_HTTP_CONNECTION

_LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-ancestors
class Http(System, Network, MotionDetection, Snapshot,
           UserManagement, Event, Audio, Record, Video,
           Log, Ptz, Special, Storage, Nas):

    def __init__(self, host, port, user,
                 password, verbose=True, protocol='http',
                 retries_connection=None, timeout_protocol=None):

        self._host = clean_url(host)
        self._port = port
        self._user = user
        self._password = password
        self._verbose = verbose
        self._protocol = protocol
        self._base_url = self.__base_url()

        self._retries_default = (
            retries_connection or MAX_RETRY_HTTP_CONNECTION)
        self._timeout_default = timeout_protocol or TIMEOUT_HTTP_PROTOCOL

        self._token = self._generate_token()
        self._set_name()

    def get_session(self, max_retries=None):
        session = requests.Session()
        max_retries = max_retries or self._retries_default
        adapter = HTTPAdapter(max_retries=max_retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _generate_token(self):
        """Create authentation to use with requests."""
        session = self.get_session()
        url = self.__base_url('magicBox.cgi?action=getMachineName')
        try:
            # try old basic method
            auth = requests.auth.HTTPBasicAuth(self._user, self._password)
            req = session.get(url, auth=auth, timeout=self._timeout_default)
            if not req.ok:
                # try new digest method
                auth = requests.auth.HTTPDigestAuth(
                    self._user, self._password)
                req = session.get(
                    url, auth=auth, timeout=self._timeout_default)
            req.raise_for_status()
        except requests.RequestException as error:
            _LOGGER.error(error)
            raise CommError('Could not communicate with camera')

        # check if user passed
        result = req.text.lower()
        if 'invalid' in result or 'error' in result:
            _LOGGER.error('Result from camera: %s',
                          req.text.strip().replace('\r\n', ': '))
            raise LoginError('Invalid credentials')

        return auth

    def _set_name(self):
        """Set device name."""
        try:
            self._name = pretty(self.machine_name)
            self._serial = self.serial_number
        except AttributeError:
            self._name = None
            self._serial = None

    def __repr__(self):
        """Default object representation."""
        return "<{0}: {1}>".format(self._name, self._serial)

    def as_dict(self):
        """Callback for __dict__."""
        cdict = self.__dict__.copy()
        redacted = '**********'
        cdict['_token'] = redacted
        cdict['_password'] = redacted
        return cdict

    # Base methods
    def __base_url(self, param=""):
        return '%s://%s:%s/cgi-bin/%s' % (self._protocol, self._host,
                                          str(self._port), param)

    def get_base_url(self):
        return self._base_url

    def command(self, cmd, retries=None, timeout_cmd=None):
        """
        Args:
            cmd - command to execute via http
            timeout_cmd - timeout, default 3sec
            retries - maximum number of retries each connection should attempt
        """
        retries = retries or self._retries_default
        timeout = timeout_cmd or self._timeout_default

        session = self.get_session(retries)
        url = self.__base_url(cmd)
        for loop in range(1, 2 + retries):
            _LOGGER.debug("Running query attempt %s", loop)
            try:
                resp = session.get(
                    url,
                    auth=self._token,
                    stream=True,
                    timeout=timeout,
                )
                resp.raise_for_status()
                break
            except requests.RequestException as error:
                if loop <= retries:
                    _LOGGER.warning("Trying again due to error %s", error)
                    continue
                else:
                    _LOGGER.error("Query failed due to error %s", error)
                    raise CommError('Could not communicate with camera')

        _LOGGER.debug("Query worked. Exit code: <%s>", resp.status_code)
        return resp

    def command_audio(self, cmd, file_content, http_header,
                      timeout=None):
        url = self.__base_url(cmd)

        timeout = timeout or self._timeout_default

        try:
            requests.post(
                url,
                files=file_content,
                auth=self._token,
                headers=http_header,
                timeout=timeout
            )
        except requests.exceptions.ReadTimeout:
            pass
