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

_LOGGER = logging.getLogger(__name__)
# fmt: off


class Media(object):

    def factory_create(self):
        ret = self.command(
            'mediaFileFind.cgi?action=factory.create'
        )
        return ret.content.decode('utf-8')

    def factory_close(self, factory_id):
        ret = self.command(
            'mediaFileFind.cgi?action=factory.close&object={0}'
            .format(factory_id)
        )
        return ret.content.decode('utf-8')

    def factory_destroy(self, factory_id):
        ret = self.command(
            'mediaFileFind.cgi?action=factory.destroy&object={0}'
            .format(factory_id)
        )
        return ret.content.decode('utf-8')

    def media_file_find_start(self, factory_id,
                              start_time, end_time, channel=0,
                              directories=(), types=(), flags=(),
                              events=(), stream=None):
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

        c_dirs = ''.join(['&condition.Dirs[{0}]={1}'.format(k, v)
                          for k, v in enumerate(directories)])

        c_types = ''.join(['&condition.Types[{0}]={1}'.format(k, v)
                           for k, v in enumerate(types)])

        c_flag = ''.join(['&condition.Flag[{0}]={1}'.format(k, v)
                          for k, v in enumerate(flags)])

        c_events = ''.join(['&condition.Events[{0}]={1}'.format(k, v)
                            for k, v in enumerate(events)])

        c_vs = ('&condition.VideoStream={0}'.format(stream) if stream else '')

        ret = self.command(
            'mediaFileFind.cgi?action=findFile&object={0}&condition.Channel'
            '={1}&condition.StartTime={2}&condition.EndTime={3}{4}{5}{6}{7}{8}'
            .format(factory_id, channel, start_time, end_time, c_dirs, c_types,
                    c_flag, c_events, c_vs)
        )
        return ret.content.decode('utf-8')

    def media_file_find_next(self, factory_id, count=100):
        ret = self.command(
            'mediaFileFind.cgi?action=findNextFile&object={0}&count={1}'
            .format(factory_id, count)
        )

        return ret.content.decode('utf-8')

    def find_files(self, start_time, end_time, channel=0,
                   directories=(), types=(), flags=(), events=(), stream=None):
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
        factory_id = self.factory_create().strip().split('=')[1]
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
            stream=stream)

        if "ok" in search.lower():
            count = 100

            while count and count > 0:
                _LOGGER.debug("%s findNextFile", self)
                content = self.media_file_find_next(factory_id)

                # The first line is 'found=N'.
                # However, it can be 'Error' if e.g. no more files found
                tag, count = (list(content.split('\r\n', 1)[0]
                                   .split('=')) + [None])[:2]
                _LOGGER.debug("%s returned %s %s", self, tag, count)

                if tag == 'found':
                    count = int(count)
                else:
                    count = None

                yield content

            self.factory_close(factory_id)
            self.factory_destroy(factory_id)
        else:
            _LOGGER.debug("%s returned error: %s", self, search)

    def download_file(self, file_path, timeout=None, stream=False):
        """
        file_path: File location like returned by FilePath from find_files()
                   Example: /mnt/sd/2019-12-31/001/dav/00/00.12.00-00.20.00.mp4
        timeout:   Use default if None
        stream:    If True use streaming download instead of
                   reading content into memory
        """
        ret = self.command(
            'RPC_Loadfile/{0}'.format(file_path),
            timeout_cmd=timeout,
            stream=stream
        )
        return ret.content

    def download_time(self, start_time, end_time, channel=0, stream=0):
        """
        start_time and end_time are formatted as yyyy-mm-dd hh:mm:ss
        '%Y-%m-%d%%20%H:%M:%S'
        """
        ret = self.command(
            'loadfile.cgi?action=startLoad&channel={0}&startTime={1}'
            '&endTime={2}&subtype={3}'
            .format(channel, start_time, end_time, stream)
        )
        return ret.content
# fmt: on
