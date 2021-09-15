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

import re
from typing import List, Optional, Tuple
from typing_extensions import TypedDict

from .http import Http
from .utils import percent, to_unit

_USED = ".UsedBytes"
_TOTAL = ".TotalBytes"


class StorageT(TypedDict):
    used_percent: str
    used: Tuple[str, str]
    total: Tuple[str, str]


class Storage(Http):
    @property
    def storage_device_info(self) -> str:
        ret = self.command("storageDevice.cgi?action=getDeviceAllInfo")
        return ret.content.decode()

    @property
    async def async_storage_device_info(self) -> str:
        ret = await self.async_command(
            "storageDevice.cgi?action=getDeviceAllInfo"
        )
        return ret.content.decode()

    @property
    def storage_device_names(self) -> str:
        ret = self.command("storageDevice.cgi?action=factory.getCollect")
        return ret.content.decode()

    @property
    async def async_storage_device_names(self) -> str:
        ret = await self.async_command(
            "storageDevice.cgi?action=factory.getCollect"
        )
        return ret.content.decode()

    @property
    def storage_used(self) -> Tuple[str, str]:
        (used,) = self._get_storage_values(self.storage_device_info, _USED)
        return to_unit(used)

    @property
    async def async_storage_used(self) -> Tuple[str, str]:
        (used,) = self._get_storage_values(
            await self.async_storage_device_info, _USED
        )
        return to_unit(used)

    @property
    def storage_total(self) -> Tuple[str, str]:
        (total,) = self._get_storage_values(self.storage_device_info, _TOTAL)
        return to_unit(total)

    @property
    async def async_storage_total(self) -> Tuple[str, str]:
        (total,) = self._get_storage_values(
            await self.async_storage_device_info, _TOTAL
        )
        return to_unit(total)

    @property
    def storage_used_percent(self) -> str:
        return self.storage_all["used_percent"]

    @property
    async def async_storage_used_percent(self) -> str:
        storage_all = await self.async_storage_all
        return storage_all["used_percent"]

    @property
    def storage_all(self) -> StorageT:
        used, total = self._get_storage_values(
            self.storage_device_info, _USED, _TOTAL
        )
        return self._build_storage_type(used, total)

    @property
    async def async_storage_all(self) -> StorageT:
        used, total = self._get_storage_values(
            await self.async_storage_device_info, _USED, _TOTAL
        )
        return self._build_storage_type(used, total)

    def _get_storage_values(self, info: str, *params) -> List[Optional[float]]:
        ret: List[Optional[float]] = []
        for param in params:
            match = re.search(f".{param}=([0-9.]+)", info)
            if match is None:
                ret.append(None)
            else:
                ret.append(float(match.group(1)))
        return ret

    def _build_storage_type(
        self, used: Optional[float], total: Optional[float]
    ) -> StorageT:
        if used is None or total is None:
            return {
                "used_percent": "unknown",
                "used": to_unit(used),
                "total": to_unit(total),
            }
        try:
            used_percent = percent(float(used), float(total))
        except (TypeError, ValueError, ZeroDivisionError):
            used_percent = "unknown"
        return {
            "used_percent": used_percent,
            "used": to_unit(used),
            "total": to_unit(total),
        }
