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


class Event(object):

    def event_handler_config(self, handlername):
        ret = self.command(
            'configManager.cgi?action=getConfig&name={0}'.format(handlername)
        )
        return ret.content.decode('utf-8')

    @property
    def alarm_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=Alarm'
        )
        return ret.content.decode('utf-8')

    @property
    def alarm_out_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=AlarmOut'
        )
        return ret.content.decode('utf-8')

    @property
    def alarm_input_channels(self):
        ret = self.command(
            'alarm.cgi?action=getInSlots'
        )
        return ret.content.decode('utf-8')

    @property
    def alarm_output_channels(self):
        ret = self.command(
            'alarm.cgi?action=getOutSlots'
        )
        return ret.content.decode('utf-8')

    @property
    def alarm_states_input_channels(self):
        ret = self.command(
            'alarm.cgi?action=getInState'
        )
        return ret.content.decode('utf-8')

    @property
    def alarm_states_output_channels(self):
        ret = self.command(
            'alarm.cgi?action=getOutState'
        )
        return ret.content.decode('utf-8')

    @property
    def video_blind_detect_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=BlindDetect'
        )
        return ret.content.decode('utf-8')

    @property
    def video_loss_detect_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=LossDetect'
        )
        return ret.content.decode('utf-8')

    @property
    def event_login_failure(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=LoginFailureAlarm'
        )
        return ret.content.decode('utf-8')

    @property
    def event_storage_not_exist(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=StorageNotExist'
        )
        return ret.content.decode('utf-8')

    @property
    def event_storage_access_failure(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=StorageFailure'
        )
        return ret.content.decode('utf-8')

    @property
    def event_storage_low_space(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=StorageLowSpace'
        )
        return ret.content.decode('utf-8')

    @property
    def event_net_abort(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=NetAbort'
        )
        return ret.content.decode('utf-8')

    @property
    def event_ip_conflict(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=IPConflict'
        )
        return ret.content.decode('utf-8')

    def event_channels_happened(self, eventcode):
        """
        Params:

        VideoMotion: motion detection event
        VideoLoss: video loss detection event
        VideoBlind: video blind detection event
        AlarmLocal: alarm detection event
        StorageNotExist: storage not exist event
        StorageFailure: storage failure event
        StorageLowSpace: storage low space event
        AlarmOutput: alarm output event
        """
        ret = self.command(
            'eventManager.cgi?action=getEventIndexes&code={0}'.format(
                eventcode)
        )
        return ret.content.decode('utf-8')

    @property
    def is_motion_detected(self):
        event = self.event_channels_happened('VideoMotion')
        if 'channels' not in event:
            return False
        return True

    @property
    def event_management(self):
        ret = self.command(
            'eventManager.cgi?action=getCaps'
        )
        return ret.content.decode('utf-8')
