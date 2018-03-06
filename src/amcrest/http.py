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

from amcrest.utils import clean_url, pretty

from amcrest.audio import Audio
from amcrest.event import Event
from amcrest.log import Log
from amcrest.motion_detection import MotionDetection
from amcrest.nas import Nas
from amcrest.network import Network
from amcrest.ptz import Ptz
from amcrest.record import Record
from amcrest.snapshot import Snapshot
from amcrest.special import Special
from amcrest.storage import Storage
from amcrest.system import System
from amcrest.user_management import UserManagement
from amcrest.video import Video

from amcrest.config import TIMEOUT_HTTP_PROTOCOL, MAX_RETRY_HTTP_CONNECTION

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

        if timeout_protocol is None:
            self._timeout_protocol = TIMEOUT_HTTP_PROTOCOL
        else:
            self._timeout_protocol = timeout_protocol

        if retries_connection is None:
            self._retries_conn = MAX_RETRY_HTTP_CONNECTION
        else:
            self._retries_conn = retries_connection

        self._token = self._generate_token()
        self._set_name()

    def _generate_token(self):
        """Discover which authentication method to use.

        Latest firmwares requires HttpDigestAuth
        Older firmwares requires HttpBasicAuth
        """
        url = self.__base_url('magicBox.cgi?action=getMachineName')
        try:
            # try old firmware first to force 401 if fails
            self._authentication = 'basic'
            auth = requests.auth.HTTPBasicAuth(self._user, self._password)
            req = requests.get(url, auth=auth)
            req.raise_for_status()

        except requests.HTTPError:
            # if 401, then try new digest method
            self._authentication = 'digest'
            auth = requests.auth.HTTPDigestAuth(self._user, self._password)
            req = requests.get(url, auth=auth)
            req.raise_for_status()

            # check if user passed
            if 'invalid' in req.text.lower() or \
               'error' in req.text.lower():
                _LOGGER.info("%s Invalid credentials", req.text)
                raise
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
        if timeout_cmd is not None:
            self._timeout_protocol = timeout_cmd

        if retries is not None:
            self._retries_conn = retries

        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=self._retries_conn))
        session.mount('https://', HTTPAdapter(max_retries=self._retries_conn))

        url = self.__base_url(cmd)
        resp = None
        loop = 0
        while loop <= self._retries_conn:
            loop += 1
            _LOGGER.debug("Running query attempt %s", loop)
            try:
                resp = session.get(
                    url,
                    auth=self._token,
                    stream=True,
                    timeout=self._timeout_protocol,
                )
                resp.raise_for_status()
                break
            except requests.HTTPError as error:
                _LOGGER.debug("Trying again due error %s", error)
                continue

            # keep the loop when 401
            if resp.status_code == 401:
                continue

        # if we got here, let's raise because it did not work
        if resp is None:
            raise ValueError('Something went wrong!!!!')

        _LOGGER.debug("Query worked. Exit code: <%s>", resp.status_code)
        return resp

    def command_audio(self, cmd, file_content, http_header,
                      timeout=None):
        url = self.__base_url(cmd)

        if timeout is not None:
            timeout = self._timeout_protocol

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
