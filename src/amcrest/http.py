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
import re
import socket
import threading
from typing import Optional, Tuple, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.connection import HTTPConnection

from .config import (
    KEEPALIVE_COUNT,
    KEEPALIVE_IDLE,
    KEEPALIVE_INTERVAL,
    MAX_RETRY_HTTP_CONNECTION,
    TIMEOUT_HTTP_PROTOCOL,
)
from .exceptions import CommError, LoginError
from .utils import clean_url, pretty

_LOGGER = logging.getLogger(__name__)

_KEEPALIVE_OPTS = HTTPConnection.default_socket_options + [
    (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
]
# On some systems TCP_KEEP* are not defined in socket.
try:
    _KEEPALIVE_OPTS += [
        (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, KEEPALIVE_IDLE),
        (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, KEEPALIVE_INTERVAL),
        (socket.IPPROTO_TCP, socket.TCP_KEEPCNT, KEEPALIVE_COUNT),
    ]
except AttributeError:
    pass

TimeoutT = Union[Optional[float], Tuple[Optional[float], Optional[float]]]


class SOHTTPAdapter(HTTPAdapter):
    """HTTPAdapter with support for socket options."""

    def __init__(self, *args, **kwargs) -> None:
        self.socket_options = kwargs.pop("socket_options", None)
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs) -> None:
        if self.socket_options is not None:
            kwargs["socket_options"] = self.socket_options
        super().init_poolmanager(*args, **kwargs)


class Http:
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        *,
        verbose: bool = True,
        protocol: str = "http",
        ssl_verify: bool = True,
        retries_connection: Optional[int] = None,
        timeout_protocol: TimeoutT = None,
    ) -> None:
        self._token_lock = threading.Lock()
        self._cmd_id_lock = threading.Lock()
        self._cmd_id = 0
        self._host = clean_url(host)
        self._port = port
        self._user = user
        self._password = password
        self._verbose = verbose
        self._protocol = protocol
        self._verify = ssl_verify
        self._base_url = self.__base_url()

        self._retries_default = (
            retries_connection
            if retries_connection is not None
            else MAX_RETRY_HTTP_CONNECTION
        )
        self._timeout_default = timeout_protocol or TIMEOUT_HTTP_PROTOCOL

        self._token: Optional[requests.auth.AuthBase] = None
        self._name: Optional[str] = None
        self._serial: Optional[str] = None

    def _generate_token(self) -> None:
        """Create authentation to use with requests."""
        cmd = "magicBox.cgi?action=getMachineName"
        _LOGGER.debug("%s Trying Basic Authentication", self)
        self._token = requests.auth.HTTPBasicAuth(self._user, self._password)
        try:
            try:
                resp = self._command(cmd).content.decode()
            except LoginError:
                _LOGGER.debug("%s Trying Digest Authentication", self)
                self._token = requests.auth.HTTPDigestAuth(
                    self._user, self._password
                )
                resp = self._command(cmd).content.decode()
        except CommError:
            self._token = None
            raise

        # check if user passed
        result = resp.lower()
        if "invalid" in result or "error" in result:
            _LOGGER.debug(
                "%s Result from camera: %s",
                self,
                resp.strip().replace("\r\n", ": "),
            )
            self._token = None
            raise LoginError("Invalid credentials")

        self._name = pretty(resp.strip())

        _LOGGER.debug("%s Retrieving serial number", self)
        self._serial = pretty(
            self._command("magicBox.cgi?action=getSerialNo")
            .content.decode()
            .strip()
        )

    def __repr__(self) -> str:
        """Default object representation."""
        if self._name is None:
            return f"<Unconnected @ {self._host}>"
        if self._serial is None:
            return f"<{self._name}:CONNECTING>"
        return f"<{self._name}:{self._serial}>"

    def as_dict(self) -> dict:
        """Callback for __dict__."""
        cdict = self.__dict__.copy()
        redacted = "**********"
        if cdict["_token"] is not None:
            cdict["_token"] = redacted
        cdict["_password"] = redacted
        return cdict

    # Base methods
    def __base_url(self, param: str = "") -> str:
        return f"{self._protocol}://{self._host}:{self._port}/cgi-bin/{param}"

    def get_base_url(self) -> str:
        return self._base_url

    def command(self, *args, **kwargs) -> requests.Response:
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
        return self._command(*args, **kwargs)

    def _command(
        self,
        cmd: str,
        retries: Optional[int] = None,
        timeout_cmd: TimeoutT = None,
        stream: bool = False,
    ) -> requests.Response:
        url = self.__base_url(cmd)
        with self._cmd_id_lock:
            cmd_id = self._cmd_id = self._cmd_id + 1
        _LOGGER.debug("%s HTTP query %i: %s", self, cmd_id, url)
        if retries is None:
            retries = self._retries_default
        timeout = timeout_cmd or self._timeout_default
        with requests.Session() as session:
            if isinstance(timeout, float):
                use_keepalive = False
            else:
                use_keepalive = timeout[0] is None or timeout[1] is None
            if use_keepalive:
                session.mount(
                    "{0}://".format(self._protocol),
                    SOHTTPAdapter(socket_options=_KEEPALIVE_OPTS),
                )
            for loop in range(1, 2 + retries):
                _LOGGER.debug(
                    "%s Running query %i attempt %s", self, cmd_id, loop
                )
                try:
                    resp = session.get(
                        url,
                        auth=self._token,
                        stream=stream,
                        timeout=timeout,
                        verify=self._verify,
                    )
                    if resp.status_code == 401:
                        _LOGGER.debug(
                            "%s Query %i: Unauthorized (401)", self, cmd_id
                        )
                        self._token = None
                        raise LoginError()
                    resp.raise_for_status()
                except requests.RequestException as error:
                    _LOGGER.debug(
                        "%s Query %i failed due to error: %r",
                        self,
                        cmd_id,
                        error,
                    )
                    if loop > retries:
                        raise CommError(error) from error
                    msg = re.sub(
                        r"at 0x[0-9a-fA-F]+", "at ADDRESS", repr(error)
                    )
                    _LOGGER.warning(
                        "%s Trying again due to error: %s", self, msg
                    )
                    continue
                else:
                    break

        _LOGGER.debug(
            "%s Query %i worked. Exit code: <%s>",
            self,
            cmd_id,
            resp.status_code,
        )
        return resp

    def command_audio(
        self,
        cmd: str,
        file_content,
        http_header,
        timeout: TimeoutT = None,
    ) -> None:
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
                timeout=timeout or self._timeout_default,
            )
        except requests.exceptions.ReadTimeout:
            pass
