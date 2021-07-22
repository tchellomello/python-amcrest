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
import shutil
from typing import Optional, Union, overload
from typing_extensions import Literal

from urllib3.exceptions import HTTPError
from urllib3.response import HTTPResponse

from .exceptions import CommError
from .http import Http, TimeoutT

_LOGGER = logging.getLogger(__name__)


class Snapshot(Http):
    def __get_config(self, config_name: str) -> str:
        ret = self.command(
            f"configManager.cgi?action=getConfig&name={config_name}"
        )
        return ret.content.decode()

    @property
    def snapshot_config(self) -> str:
        return self.__get_config("Snap")

    @overload
    def snapshot(
        self,
        *,
        channel: Optional[int] = ...,
        path_file: Optional[str] = ...,
        timeout: TimeoutT = ...,
        stream: Literal[True] = ...,
    ) -> HTTPResponse:
        ...

    @overload
    def snapshot(
        self,
        *,
        channel: Optional[int] = ...,
        path_file: Optional[str] = ...,
        timeout: TimeoutT = ...,
        stream: Literal[False] = ...,
    ) -> bytes:
        ...

    def snapshot(
        self,
        *,
        channel: Optional[int] = None,
        path_file: Optional[str] = None,
        timeout: TimeoutT = None,
        stream: bool = True,
    ) -> Union[bytes, HTTPResponse]:
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
            cmd += f"?channel={channel}"
        ret = self.command(cmd, timeout_cmd=timeout, stream=stream)

        if path_file:
            with open(path_file, "wb") as out_file:
                if stream:
                    try:
                        shutil.copyfileobj(ret.raw, out_file)
                    except HTTPError as error:
                        _LOGGER.debug(
                            "%s Snapshot to file failed due to error: %s",
                            self,
                            repr(error),
                        )
                        raise CommError(error) from error
                else:
                    out_file.write(ret.content)

        return ret.raw if stream else ret.content
