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

from datetime import datetime
from typing import AsyncIterator, Iterator

from .http import Http
from .utils import date_to_str


class Log(Http):
    def log_clear_all(self) -> str:
        ret = self.command("log.cgi?action=clear")
        return ret.content.decode()

    async def async_log_clear_all(self) -> str:
        ret = await self.async_command("log.cgi?action=clear")
        return ret.content.decode()

    def log_show(self, start_time: datetime, end_time: datetime) -> str:
        start = date_to_str(start_time)
        end = date_to_str(end_time)
        ret = self.command(
            "Log.backup?action=All&"
            f"condition.StartTime={start}&condition.EndTime={end}"
        )
        return ret.content.decode()

    async def async_log_show(
        self, start_time: datetime, end_time: datetime
    ) -> str:
        start = date_to_str(start_time)
        end = date_to_str(end_time)
        ret = await self.async_command(
            "Log.backup?action=All&"
            f"condition.StartTime={start}&condition.EndTime={end}"
        )
        return ret.content.decode()

    def log_find_start(self, start_time: datetime, end_time: datetime) -> str:
        start = date_to_str(start_time)
        end = date_to_str(end_time)
        ret = self.command(
            "log.cgi?action=startFind&"
            f"condition.StartTime={start}&condition.EndTime={end}"
        )

        return ret.content.decode()

    async def async_log_find_start(
        self, start_time: datetime, end_time: datetime
    ) -> str:
        start = date_to_str(start_time)
        end = date_to_str(end_time)
        ret = await self.async_command(
            "log.cgi?action=startFind&"
            f"condition.StartTime={start}&condition.EndTime={end}"
        )

        return ret.content.decode()

    def log_find_next(self, token: str, count: int = 100) -> str:
        ret = self.command(
            f"log.cgi?action=doFind&token={token}&count={count}"
        )
        return ret.content.decode()

    async def async_log_find_next(self, token: str, count: int = 100) -> str:
        ret = await self.async_command(
            f"log.cgi?action=doFind&token={token}&count={count}"
        )
        return ret.content.decode()

    def log_find_stop(self, token: str) -> str:
        ret = self.command(f"log.cgi?action=stopFind&token={token}")
        return ret.content.decode()

    async def async_log_find_stop(self, token: str) -> str:
        ret = await self.async_command(
            f"log.cgi?action=stopFind&token={token}"
        )
        return ret.content.decode()

    def log_find(
        self, start_time: datetime, end_time: datetime
    ) -> Iterator[str]:
        token = self.log_find_start(start_time, end_time).strip().split("=")[1]

        while True:
            content = self.log_find_next(token)
            tag, _, count = content.split("\r\n", 1)[0].partition("=")

            yield content

            if tag != "found" or int(count) == 0:
                break

        self.log_find_stop(token)

    async def async_log_find(
        self, start_time: datetime, end_time: datetime
    ) -> AsyncIterator[str]:
        token = (
            (await self.async_log_find_start(start_time, end_time))
            .strip()
            .split("=")[1]
        )

        while True:
            content = await self.async_log_find_next(token)
            tag, _, count = content.split("\r\n", 1)[0].partition("=")

            yield content

            if tag != "found" or int(count) == 0:
                break

        await self.async_log_find_stop(token)
