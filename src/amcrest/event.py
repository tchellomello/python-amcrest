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
from typing import (
    Any,
    AsyncIterator,
    AsyncIterable,
    Dict,
    Iterator,
    Iterable,
    List,
    Optional,
    Tuple,
)

from requests import RequestException
from urllib3.exceptions import HTTPError

from .exceptions import CommError
from .http import Http, TimeoutT
from .utils import pretty

_LOGGER = logging.getLogger(__name__)
_REG_PARSE_KEY_VALUE = re.compile(r"(?P<key>.+?)(?:=)(?P<value>.+?)(?:;|$)")
_REG_PARSE_MALFORMED_JSON = re.compile(
    r'(?P<key>"[^"\\]*(?:\\.[^"\\]*)*"|[^\s"]+)\s:\s(?P<value>"[^"\\]*(?:\\.[^"\\]*)*"|[^\s"]+)'
)


def _event_lines(ret: Iterable[str]) -> Iterator[str]:
    line = []
    for char in ret:
        line.append(char)
        if line[-2:] == ["\r", "\n"]:
            yield "".join(line).strip()
            line.clear()


async def _async_event_lines(ret: AsyncIterable[str]) -> AsyncIterator[str]:
    line = []
    async for char in ret:
        line.append(char)
        if line[-2:] == ["\r", "\n"]:
            yield "".join(line).strip()
            line.clear()


class Event(Http):
    def event_handler_config(self, handlername: str) -> str:
        return self._get_config(handlername)

    async def async_event_handler_config(self, handlername: str) -> str:
        return await self._async_get_config(handlername)

    def alarm_handler(self, alarm_name: str) -> str:
        ret = self.command("alarm.cgi?action={alarm_name}")
        return ret.content.decode()

    async def async_alarm_handler(self, alarm_name: str) -> str:
        ret = await self.async_command("alarm.cgi?action={alarm_name}")
        return ret.content.decode()

    @property
    def alarm_config(self) -> str:
        return self.event_handler_config("Alarm")

    @property
    async def async_alarm_config(self) -> str:
        return await self.async_event_handler_config("Alarm")

    @property
    def alarm_out_config(self) -> str:
        return self.event_handler_config("AlarmOut")

    @property
    async def async_alarm_out_config(self) -> str:
        return await self.async_event_handler_config("AlarmOut")

    @property
    def alarm_input_channels(self) -> str:
        return self.alarm_handler("getInSlots")

    @property
    async def async_alarm_input_channels(self) -> str:
        return await self.async_alarm_handler("getInSlots")

    @property
    def alarm_output_channels(self) -> str:
        return self.alarm_handler("getOutSlots")

    @property
    async def async_alarm_output_channels(self) -> str:
        return await self.async_alarm_handler("getOutSlots")

    @property
    def alarm_states_input_channels(self) -> str:
        return self.alarm_handler("getInState")

    @property
    async def async_alarm_states_input_channels(self) -> str:
        return await self.async_alarm_handler("getInState")

    @property
    def alarm_states_output_channels(self) -> str:
        return self.alarm_handler("getOutState")

    @property
    async def async_alarm_states_output_channels(self) -> str:
        return await self.async_alarm_handler("getOutState")

    @property
    def video_blind_detect_config(self) -> str:
        return self.event_handler_config("BlindDetect")

    @property
    async def async_video_blind_detect_config(self) -> str:
        return await self.async_event_handler_config("BlindDetect")

    @property
    def video_loss_detect_config(self) -> str:
        return self.event_handler_config("LossDetect")

    @property
    async def async_video_loss_detect_config(self) -> str:
        return await self.async_event_handler_config("LossDetect")

    @property
    def event_login_failure(self) -> str:
        return self.event_handler_config("LoginFailureAlarm")

    @property
    async def async_event_login_failure(self) -> str:
        return await self.async_event_handler_config("LoginFailureAlarm")

    @property
    def event_storage_not_exist(self) -> str:
        return self.event_handler_config("StorageNotExist")

    @property
    async def async_event_storage_not_exist(self) -> str:
        return await self.async_event_handler_config("StorageNotExist")

    @property
    def event_storage_access_failure(self) -> str:
        return self.event_handler_config("StorageFailure")

    @property
    async def async_event_storage_access_failure(self) -> str:
        return await self.async_event_handler_config("StorageFailure")

    @property
    def event_storage_low_space(self) -> str:
        return self.event_handler_config("StorageLowSpace")

    @property
    async def async_event_storage_low_space(self) -> str:
        return await self.async_event_handler_config("StorageLowSpace")

    @property
    def event_net_abort(self) -> str:
        return self.event_handler_config("NetAbort")

    @property
    async def async_event_net_abort(self) -> str:
        return await self.async_event_handler_config("NetAbort")

    @property
    def event_ip_conflict(self) -> str:
        return self.event_handler_config("IPConflict")

    @property
    async def async_event_ip_conflict(self) -> str:
        return await self.async_event_handler_config("IPConflict")

    def event_channels_happened(self, eventcode: str) -> List[int]:
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
            f"eventManager.cgi?action=getEventIndexes&code={eventcode}"
        )
        output = ret.content.decode()
        if "Error" in output:
            return []
        return [int(pretty(channel)) for channel in output.split()]

    async def async_event_channels_happened(self, eventcode: str) -> List[int]:
        ret = await self.async_command(
            f"eventManager.cgi?action=getEventIndexes&code={eventcode}"
        )
        output = ret.content.decode()
        if "Error" in output:
            return []
        return [int(pretty(channel)) for channel in output.split()]

    @property
    def is_motion_detected(self) -> List[int]:
        return self.event_channels_happened("VideoMotion")

    @property
    async def async_is_motion_detected(self) -> List[int]:
        return await self.async_event_channels_happened("VideoMotion")

    @property
    def is_alarm_triggered(self) -> List[int]:
        return self.event_channels_happened("AlarmLocal")

    @property
    async def async_is_alarm_triggered(self) -> List[int]:
        return await self.async_event_channels_happened("AlarmLocal")

    @property
    def is_human_detected(self) -> List[int]:
        return self.event_channels_happened("SmartMotionHuman")

    @property
    async def async_is_human_detected(self) -> List[int]:
        return await self.async_event_channels_happened("SmartMotionHuman")

    @property
    def is_vehicle_detected(self) -> List[int]:
        return self.event_channels_happened("SmartMotionVehicle")

    @property
    async def async_is_vehicle_detected(self) -> List[int]:
        return await self.async_event_channels_happened("SmartMotionVehicle")

    @property
    def event_management(self) -> str:
        ret = self.command("eventManager.cgi?action=getCaps")
        return ret.content.decode()

    @property
    async def async_event_management(self) -> str:
        ret = await self.async_command("eventManager.cgi?action=getCaps")
        return ret.content.decode()

    def event_stream(
        self,
        eventcodes: str,
        *,
        retries: Optional[int] = None,
        timeout_cmd: TimeoutT = None,
    ) -> Iterator[str]:
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
            if isinstance(self._timeout_default, tuple):
                timeout_cmd = self._timeout_default[0], None
            else:
                timeout_cmd = self._timeout_default, None

        ret = self.command(
            f"eventManager.cgi?action=attach&codes=[{eventcodes}]",
            retries=retries,
            timeout_cmd=timeout_cmd,
            stream=True,
        )
        if ret.encoding is None:
            ret.encoding = "utf-8"  # type: ignore[unreachable]

        try:
            for line in _event_lines(ret.iter_content(decode_unicode=True)):
                if line.lower().startswith("content-length:"):
                    chunk_size = int(line.split(":")[1])
                    try:
                        yield next(
                            ret.iter_content(
                                chunk_size=chunk_size, decode_unicode=True
                            )
                        )
                    except StopIteration:
                        return
        except (RequestException, HTTPError) as error:
            _LOGGER.debug("%s Error during event streaming: %r", self, error)
            raise CommError(error) from error
        finally:
            ret.close()

    async def async_event_stream(
        self, eventcodes: str, *, timeout_cmd: TimeoutT = None
    ) -> AsyncIterator[str]:
        """Return a stream of event info lines."""
        # If timeout is not specified, then use default, but remove read
        # timeout since there's no telling when, if ever, an event will come.
        if timeout_cmd is None:
            if isinstance(self._timeout_default, tuple):
                timeout_cmd = self._timeout_default[0], None
            else:
                timeout_cmd = self._timeout_default, None

        async with self.async_stream_command(
            f"eventManager.cgi?action=attach&codes=[{eventcodes}]",
            timeout_cmd=timeout_cmd,
        ) as ret:
            it = ret.aiter_text(chunk_size=1)
            async for line in _async_event_lines(it):
                if line.lower().startswith("content-length:"):
                    chunk_size = int(line.split(":")[1])
                    chars = []
                    async for char in it:
                        chars.append(char)
                        if len(chars) == chunk_size:
                            break
                    else:
                        # If we can't get the chunk, then return out
                        return
                    yield "".join(chars)

    def event_actions(
        self,
        eventcodes: str,
        retries: Optional[int] = None,
        timeout_cmd: TimeoutT = None,
    ) -> Iterator[Tuple[str, Dict[str, Any]]]:
        """Return a stream of event (code, payload) tuples."""
        for event_info in self.event_stream(
            eventcodes, retries=retries, timeout_cmd=timeout_cmd
        ):
            payload = self._build_payload(event_info)
            yield payload["Code"], payload

    async def async_event_actions(
        self, eventcodes: str, timeout_cmd: TimeoutT = None
    ) -> AsyncIterator[Tuple[str, Dict[str, Any]]]:
        """Return a stream of event (code, payload) tuples."""
        async for event_info in self.async_event_stream(
            eventcodes, timeout_cmd=timeout_cmd
        ):
            payload = self._build_payload(event_info)
            yield payload["Code"], payload

    def _build_payload(self, event_info: str) -> Dict[str, Any]:
        _LOGGER.debug("%s event info: %r", self, event_info)
        payload = {}
        for key, value in _REG_PARSE_KEY_VALUE.findall(
            event_info.strip().replace("\n", "")
        ):
            if key == "data":
                value = {
                    data_key.replace('"', ""): data_value.replace('"', "")
                    for data_key, data_value in _REG_PARSE_MALFORMED_JSON.findall(
                        value
                    )
                }
            payload[key] = value
        _LOGGER.debug(
            "%s generate new event, code: %s , payload: %s",
            self,
            payload["Code"],
            payload,
        )
        return payload


class NoHeaderErrorFilter(logging.Filter):
    """
    Filter out urllib3 Header Parsing Errors due to a urllib3 bug.

    See https://github.com/urllib3/urllib3/issues/800
    """

    def filter(self, record):
        """Filter out Header Parsing Errors."""
        return "Failed to parse headers" not in record.getMessage()
