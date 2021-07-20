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
from datetime import datetime
from typing import Iterator, Optional, Sequence

from .http import Http, TimeoutT
from .utils import date_to_str

_LOGGER = logging.getLogger(__name__)


class Media(Http):
    def factory_create(self) -> str:
        ret = self.command("mediaFileFind.cgi?action=factory.create")
        return ret.content.decode()

    def factory_close(self, factory_id: str) -> str:
        ret = self.command(
            f"mediaFileFind.cgi?action=factory.close&object={factory_id}"
        )
        return ret.content.decode()

    def factory_destroy(self, factory_id: str) -> str:
        ret = self.command(
            f"mediaFileFind.cgi?action=factory.destroy&object={factory_id}"
        )
        return ret.content.decode()

    def media_file_find_start(
        self,
        factory_id: str,
        start_time: datetime,
        end_time: datetime,
        channel: int = 0,
        directories: Sequence[str] = (),
        types: Sequence[str] = (),
        flags: Sequence[str] = (),
        events: Sequence[str] = (),
        stream: Optional[str] = None,
    ) -> str:
        """
        https://s3.amazonaws.com/amcrest-files/Amcrest+HTTP+API+3.2017.pdf

        factory_id : returned by factory_create()

        dir : in which directories you want to find the file. It is an array.
                The index starts from 1. The range of dir is {"/mnt/dvr/sda0",
                "/mnt/dvr/sda1"}. This condition can be omitted. If omitted,
                find files in all the directories.

        type : which types of the file you want to find. It is an array. The
                index starts from 0. The range of type is {"dav", "jpg", "mp4"}
                If omitted, find files with all the types.

        flag : which flags of the file you want to find. It is an array. The
                index starts from 0. The range of flag is {"Timing", "Manual",
                "Marker", "Event", "Mosaic", "Cutout"}. If omitted, find files
                with all the flags.

        event : by which event the record file is triggered. It is an array.
                The index starts from 0. The range of event is {"AlarmLocal",
                "VideoMotion", "VideoLoss", "VideoBlind", "Traffic*"}. This
                condition can be omitted. If omitted, find files of all the
                events. stream : which video stream type you want to find.
                The range of stream is {"Main", "Extra1", "Extra2", "Extra3"}.
                If omitted, find files with all the stream types.
        """

        c_dirs = "".join(
            f"&condition.Dirs[{k}]={v}" for k, v in enumerate(directories)
        )

        c_types = "".join(
            f"&condition.Types[{k}]={v}" for k, v in enumerate(types)
        )

        c_flag = "".join(
            f"&condition.Flag[{k}]={v}" for k, v in enumerate(flags)
        )

        c_events = "".join(
            f"&condition.Events[{k}]={v}" for k, v in enumerate(events)
        )

        c_vs = f"&condition.VideoStream={stream}" if stream else ""

        start = date_to_str(start_time)
        end = date_to_str(end_time)
        extra_cond = "".join([c_dirs, c_types, c_flag, c_events, c_vs])
        ret = self.command(
            f"mediaFileFind.cgi?action=findFile&object={factory_id}&"
            f"condition.Channel={channel}&condition.StartTime={start}&"
            f"condition.EndTime={end}{extra_cond}"
        )
        return ret.content.decode()

    def media_file_find_next(self, factory_id: str, count: int = 100) -> str:
        ret = self.command(
            "mediaFileFind.cgi?action=findNextFile&"
            f"object={factory_id}&count={count}"
        )

        return ret.content.decode()

    def find_files(
        self,
        start_time: datetime,
        end_time: datetime,
        channel: int = 0,
        directories: Sequence[str] = (),
        types: Sequence[str] = (),
        flags: Sequence[str] = (),
        events: Sequence[str] = (),
        stream: Optional[str] = None,
    ) -> Iterator[str]:
        """
        https://s3.amazonaws.com/amcrest-files/Amcrest+HTTP+API+3.2017.pdf

        dir : in which directories you want to find the file. It is an array.
                The index starts from 1. The range of dir is {"/mnt/dvr/sda0",
                "/mnt/dvr/sda1"}. This condition can be omitted. If omitted,
                find files in all the directories.

        type : which types of the file you want to find. It is an array. The
                index starts from 0. The range of type is {"dav", "jpg", "mp4"}
                If omitted, find files with all the types.

        flag : which flags of the file you want to find. It is an array. The
                index starts from 0. The range of flag is {"Timing", "Manual",
                "Marker", "Event", "Mosaic", "Cutout"}. If omitted, find files
                with all the flags.

        event : by which event the record file is triggered. It is an array.
                The index starts from 0. The range of event is {"AlarmLocal",
                "VideoMotion", "VideoLoss", "VideoBlind", "Traffic*"}. This
                condition can be omitted. If omitted, find files of all the
                events. stream : which video stream type you want to find.
                The range of stream is {"Main", "Extra1", "Extra2", "Extra3"}.
                If omitted, find files with all the stream types.
        """
        factory_id = self.factory_create().strip().split("=")[1]
        _LOGGER.debug("%s findFile for factory_id=%s", self, factory_id)

        search = self.media_file_find_start(
            factory_id=factory_id,
            start_time=start_time,
            end_time=end_time,
            channel=channel,
            directories=directories,
            types=types,
            flags=flags,
            events=events,
            stream=stream,
        )

        if "ok" in search.lower():
            while True:
                _LOGGER.debug("%s findNextFile", self)
                content = self.media_file_find_next(factory_id)

                # The first line is 'found=N'.
                # However, it can be 'Error' if e.g. no more files found
                tag, _, str_count = content.split("\r\n", 1)[0].partition("=")
                if tag == "found":
                    count = int(str_count)
                else:
                    break

                _LOGGER.debug("%s returned %s %s", self, tag, count)

                if count == 0:
                    break

                yield content

            self.factory_close(factory_id)
            self.factory_destroy(factory_id)
        else:
            _LOGGER.debug("%s returned error: %s", self, search)

    def download_file(
        self,
        file_path: str,
        timeout: TimeoutT = None,
        stream: bool = False,
    ) -> bytes:
        """
        file_path: File location like returned by FilePath from find_files()
                   Example: /mnt/sd/2019-12-31/001/dav/00/00.12.00-00.20.00.mp4
        timeout:   Use default if None
        stream:    If True use streaming download instead of
                   reading content into memory
        """
        ret = self.command(
            "RPC_Loadfile/{0}".format(file_path),
            timeout_cmd=timeout,
            stream=stream,
        )
        return ret.content

    def download_time(
        self,
        start_time: datetime,
        end_time: datetime,
        channel: int = 0,
        stream: int = 0,
    ) -> bytes:
        """
        start_time and end_time are formatted as yyyy-mm-dd hh:mm:ss
        '%Y-%m-%d%%20%H:%M:%S'
        """
        start = date_to_str(start_time)
        end = date_to_str(end_time)
        ret = self.command(
            f"loadfile.cgi?action=startLoad&channel={channel}&"
            f"startTime={start}&endTime={end}&subtype={stream}"
        )
        return ret.content
