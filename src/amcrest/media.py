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

    def find_file(self, start_time, end_time, channel=0,
                  directories=[], types=[], flags=[], events=[], stream=None):
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

        ret = self.command(
            'mediaFileFind.cgi?action=findFile&object={0}&condition.Channel'
            '={1}&condition.StartTime={2}&condition.EndTime={3}'
            .format(factory_id, channel, start_time, end_time)
            + ''.join(['&condition.Dirs[{0}]={1}'.format(k, v)
                       for k, v in enumerate(directories)])
            + ''.join(['&condition.Types[{0}]={1}'.format(k, v)
                       for k, v in enumerate(types)])
            + ''.join(['&condition.Flag[{0}]={1}'.format(k, v)
                       for k, v in enumerate(flags)])
            + ''.join(['&condition.Events[{0}]={1}'.format(k, v)
                       for k, v in enumerate(events)])
            + ('&condition.VideoStream={0}'.format(stream) if stream else '')
        )
        if "ok" in ret.content.decode('utf-8').lower():
            ret = self.command(
                'mediaFileFind.cgi?action=findNextFile&object={0}&count=100'
                .format(factory_id)
            )
            self.factory_close(factory_id)
            self.factory_destroy(factory_id)

            return ret.content.decode('utf-8')

    def download_file(self, file_path):
        ret = self.command(
            'RPC_Loadfile/{0}'.format(file_path)
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
