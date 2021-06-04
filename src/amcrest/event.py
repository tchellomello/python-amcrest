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
import re

from requests import RequestException
from urllib3.exceptions import HTTPError

from .exceptions import CommError
from .utils import pretty

_LOGGER = logging.getLogger(__name__)
_REG_PARSE_KEY_VALUE = re.compile(r"(?P<key>.+?)(?:=)(?P<value>.+?)(?:;|$)")
_REG_PARSE_MALFORMED_JSON = re.compile(
    r'(?P<key>"[^"\\]*(?:\\.[^"\\]*)*"|[^\s"]+)\s:\s(?P<value>"[^"\\]*(?:\\.[^"\\]*)*"|[^\s"]+)'
)


def _event_lines(ret):
    line = []
    for char in ret.iter_content(decode_unicode=True):
        line.append(char)
        if line[-2:] == ["\r", "\n"]:
            yield "".join(line).strip()
            line.clear()


class Event(object):
    def event_handler_config(self, handlername):
        ret = self.command(
            "configManager.cgi?action=getConfig&name={0}".format(handlername)
        )
        return ret.content.decode("utf-8")

    @property
    def alarm_config(self):
        return self.event_handler_config("Alarm")

    @property
    def alarm_out_config(self):
        return self.event_handler_config("AlarmOut")

    @property
    def alarm_input_channels(self):
        ret = self.command("alarm.cgi?action=getInSlots")
        return ret.content.decode("utf-8")

    @property
    def alarm_output_channels(self):
        ret = self.command("alarm.cgi?action=getOutSlots")
        return ret.content.decode("utf-8")

    @property
    def alarm_states_input_channels(self):
        ret = self.command("alarm.cgi?action=getInState")
        return ret.content.decode("utf-8")

    @property
    def alarm_states_output_channels(self):
        ret = self.command("alarm.cgi?action=getOutState")
        return ret.content.decode("utf-8")

    @property
    def video_blind_detect_config(self):
        return self.event_handler_config("BlindDetect")

    @property
    def video_loss_detect_config(self):
        return self.event_handler_config("LossDetect")

    @property
    def event_login_failure(self):
        return self.event_handler_config("LoginFailureAlarm")

    @property
    def event_storage_not_exist(self):
        return self.event_handler_config("StorageNotExist")

    @property
    def event_storage_access_failure(self):
        return self.event_handler_config("StorageFailure")

    @property
    def event_storage_low_space(self):
        return self.event_handler_config("StorageLowSpace")

    @property
    def event_net_abort(self):
        return self.event_handler_config("NetAbort")

    @property
    def event_ip_conflict(self):
        return self.event_handler_config("IPConflict")

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
        SmartMotionHuman: human detection event
        SmartMotionVehicle: vehicle detection event
        """
        ret = self.command(
            "eventManager.cgi?action=getEventIndexes&code={0}".format(
                eventcode
            )
        )
        output = ret.content.decode()
        if "Error" in output:
            return []
        return [int(pretty(channel)) for channel in output.split()]

    @property
    def is_motion_detected(self):
        return self.event_channels_happened("VideoMotion")

    @property
    def is_alarm_triggered(self):
        return self.event_channels_happened("AlarmLocal")

    @property
    def is_human_detected(self):
        return self.event_channels_happened("SmartMotionHuman")

    @property
    def is_vehicle_detected(self):
        return self.event_channels_happened("SmartMotionVehicle")

    @property
    def event_management(self):
        ret = self.command("eventManager.cgi?action=getCaps")
        return ret.content.decode("utf-8")

    def event_stream(self, eventcodes, retries=None, timeout_cmd=None):
        """
        Return a stream of event info lines.

        eventcodes: One or more event codes separated by commas with no spaces

        VideoMotion: motion detection event
        VideoLoss: video loss detection event
        VideoBlind: video blind detection event
        AlarmLocal: alarm detection event
        StorageNotExist: storage not exist event
        StorageFailure: storage failure event
        StorageLowSpace: storage low space event
        AlarmOutput: alarm output event
        SmartMotionHuman: human detection event
        SmartMotionVehicle: vehicle detection event
        """
        urllib3_logger = logging.getLogger("urllib3.connectionpool")
        if not any(
            isinstance(x, NoHeaderErrorFilter) for x in urllib3_logger.filters
        ):
            urllib3_logger.addFilter(NoHeaderErrorFilter())

        # If timeout is not specified, then use default, but remove read
        # timeout since there's no telling when, if ever, an event will come.
        if timeout_cmd is None:
            try:
                timeout_cmd = (self._timeout_default[0], None)
            except TypeError:
                timeout_cmd = (self._timeout_default, None)

        ret = self.command(
            "eventManager.cgi?action=attach&codes=[{0}]".format(eventcodes),
            retries=retries,
            timeout_cmd=timeout_cmd,
            stream=True,
        )
        if ret.encoding is None:
            ret.encoding = "utf-8"

        try:
            for line in _event_lines(ret):
                if line.lower().startswith("content-length:"):
                    chunk_size = int(line.split(":")[1])
                    yield next(
                        ret.iter_content(
                            chunk_size=chunk_size, decode_unicode=True
                        )
                    )
        except (RequestException, HTTPError) as error:
            _LOGGER.debug("%s Error during event streaming: %r", self, error)
            raise CommError(error)
        finally:
            ret.close()

    def event_actions(self, eventcodes, retries=None, timeout_cmd=None):
        """Return a stream of event (code, payload) tuples."""
        for event_info in self.event_stream(eventcodes, retries, timeout_cmd):
            _LOGGER.debug("%s event info: %r", self, event_info)
            payload = {}
            for Key, Value in _REG_PARSE_KEY_VALUE.findall(
                event_info.strip().replace("\n", "")
            ):
                if Key == "data":
                    Value = {
                        DataKey.replace('"', ""): DataValue.replace('"', "")
                        for DataKey, DataValue in _REG_PARSE_MALFORMED_JSON.findall(
                            Value
                        )
                    }
                payload[Key] = Value
            _LOGGER.debug(
                "%s generate new event, code: %s , payload: %s",
                self,
                payload["Code"],
                payload,
            )
            yield payload["Code"], payload


class NoHeaderErrorFilter(logging.Filter):
    """
    Filter out urllib3 Header Parsing Errors due to a urllib3 bug.

    See https://github.com/urllib3/urllib3/issues/800
    """

    def filter(self, record):
        """Filter out Header Parsing Errors."""
        return "Failed to parse headers" not in record.getMessage()
