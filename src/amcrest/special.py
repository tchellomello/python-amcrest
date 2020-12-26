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
from typing import Optional

from urllib3.exceptions import HTTPError  # type: ignore[import]

from .exceptions import CommError
from .http import Http

_LOGGER = logging.getLogger(__name__)


class Special(Http):
    def realtime_stream(
        self,
        channel: int = 1,
        stream_type: int = 0,
        path_file: Optional[str] = None,
    ):
        """
        If the stream is redirect to a file, use mplayer tool to
        visualize the video record

        camera.realtime_stream(path_file="/home/user/Desktop/myvideo)
        $ mplayer /home/user/Desktop/myvideo
        """
        ret = self.command(
            f"realmonitor.cgi?action=getStream&channel={channel}&subtype={stream_type}",
            stream=True,
        )

        if path_file:
            try:
                with open(path_file, "wb") as out_file:
                    shutil.copyfileobj(ret.raw, out_file)
            except HTTPError as error:
                _LOGGER.debug(
                    "%s Realtime stream capture to file failed due "
                    "to error: %s",
                    self,
                    repr(error),
                )
                raise CommError(error)

        return ret.raw

    def mjpeg_url(self, channel: int = 1, stream_type: int = 1) -> str:
        """
        Return MJPEG streaming url

        11/05/2016

        Looks like the mjpeg support was removed from the mainstream in one of
        the firmware updates, so subtype=0 is not working.

        I have tested with the below firmware and still not working
        in the mainstream:
            Amcrest_IPC-AWXX_Eng_N_V2.420.AC00.15.R.20160908.bin

        Based on above, the cmd we send to camera should use: subtype=1 until
        mainstream is back.

        Simple translation:
            subtype=0 for mainstream
            subtype=1 for substream

        Tested on device: IP2M-841B

        Users complaining here too:
        https://amcrest.com/forum/technical-discussion-f3/lost-mjpeg-encode-for-main-stream-after-firmware-u-t1516.html

        Params:
            channelno: integer, the video channel index which starts from 1,
                       default 1 if not specified.

            typeno: the stream type, default 0 if not specified. It can be
                    the following value:

                    0-Main Stream
                    1-Extra Stream 1 (Sub Stream)
                    2-Extra Stream 2 (Sub Stream)
        """
        cmd = f"{self._base_url}mjpg/video.cgi?channel={channel}&subtype={stream_type}"
        return cmd

    def mjpg_stream(
        self,
        channel: int = 1,
        stream_type: int = 1,
        path_file: Optional[str] = None,
    ):
        """
        Params:
            channelno: integer, the video channel index which starts from 1,
                       default 1 if not specified.

            typeno: the stream type, default 0 if not specified. It can be
                    the following value:

                    0-Main Stream
                    1-Extra Stream 1 (Sub Stream)
                    2-Extra Stream 2 (Sub Stream)
        """
        cmd = self.mjpeg_url(channel=channel, stream_type=stream_type)
        ret = self.command(cmd, stream=True)

        if path_file:
            try:
                with open(path_file, "wb") as out_file:
                    shutil.copyfileobj(ret.raw, out_file)
            except HTTPError as error:
                _LOGGER.debug(
                    "%s MJPEG stream capture to file failed due to error: %s",
                    self,
                    repr(error),
                )
                raise CommError(error)

        return ret.raw
