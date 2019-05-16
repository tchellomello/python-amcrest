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
import threading

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

        self._token_lock = threading.Lock()
        self._host = clean_url(host)
        self._port = port
        self._user = user
        self._password = password
        self._verbose = verbose
        self._protocol = protocol
        self._base_url = self.__base_url()

        self._retries_default = (
            retries_connection if retries_connection is not None
            else MAX_RETRY_HTTP_CONNECTION)
        self._timeout_default = timeout_protocol or TIMEOUT_HTTP_PROTOCOL

        self._token = None
        self._name = None
        self._serial = None
        # Ignore comm errors in case camera happens to be off or there are
        # temporary network issues. User can retry later and we'll get token
        # then if camera is accessible again.
        try:
            self._generate_token()
        except CommError:
            pass

    def _generate_token(self):
        """Create authentation to use with requests."""
        cmd = 'magicBox.cgi?action=getMachineName'
        _LOGGER.debug('%s Trying Basic Authentication', self)
        self._token = requests.auth.HTTPBasicAuth(self._user, self._password)
        try:
            resp = self._command(cmd).content.decode('utf-8')
        except CommError:
            _LOGGER.debug('%s Trying Digest Authentication', self)
            self._token = requests.auth.HTTPDigestAuth(
                self._user, self._password)
            try:
                resp = self._command(cmd).content.decode('utf-8')
            except CommError as error:
                self._token = None
                raise error

        # check if user passed
        result = resp.lower()
        if 'invalid' in result or 'error' in result:
            _LOGGER.debug('%s Result from camera: %s', self,
                          resp.strip().replace('\r\n', ': '))
            self._token = None
            raise LoginError('Invalid credentials')

        self._name = pretty(resp.strip())

        _LOGGER.debug('%s Retrieving serial number', self)
        self._serial = pretty(self._command(
            'magicBox.cgi?action=getSerialNo').content.decode('utf-8').strip())

    def __repr__(self):
        """Default object representation."""
        return "<{0}:{1}>".format(self._name, self._serial)

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

    def command(self, cmd, retries=None, timeout_cmd=None, stream=False):
        """
        Args:
            cmd - command to execute via http
            retries - maximum number of retries each connection should attempt
            timeout_cmd - timeout
            stream - if True do not download entire response immediately
        """
        with self._token_lock:
            if not self._token:
                self._generate_token()
        return self._command(cmd, retries, timeout_cmd, stream)

    def _command(self, cmd, retries=None, timeout_cmd=None, stream=False):
        _LOGGER.debug("%s Running query", self)
        session = requests.Session()
        max_retries = retries if retries is not None else self._retries_default
        if max_retries:
            adapter = HTTPAdapter(max_retries=max_retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
        url = self.__base_url(cmd)
        try:
            resp = session.get(
                url,
                auth=self._token,
                stream=stream,
                timeout=timeout_cmd or self._timeout_default,
            )
            resp.raise_for_status()
        except requests.RequestException as error:
            _LOGGER.debug(
                "%s Query failed due to error: %s", self, repr(error))
            raise CommError(error)

        _LOGGER.debug(
            "%s Query worked. Exit code: <%s>", self, resp.status_code)
        return resp

    def command_audio(self, cmd, file_content, http_header,
                      timeout=None):
        with self._token_lock:
            if not self._token:
                self._generate_token()
        url = self.__base_url(cmd)
        try:
            requests.post(
                url,
                files=file_content,
                auth=self._token,
                headers=http_header,
                timeout=timeout or self._timeout_default
            )
        except requests.exceptions.ReadTimeout:
            pass
