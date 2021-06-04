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
    def storage_device_names(self) -> str:
        ret = self.command("storageDevice.cgi?action=factory.getCollect")
        return ret.content.decode()

    def _get_storage_values(self, *params) -> List[Optional[float]]:
        info = self.storage_device_info
        ret: List[Optional[float]] = []
        for param in params:
            match = re.search(f".{param}=([0-9.]+)", info)
            if match is None:
                ret.append(None)
            else:
                ret.append(float(match.group(1)))
        return ret

    @property
    def storage_used(self) -> Tuple[str, str]:
        used = self._get_storage_values(_USED)[0]
        if used is None:
            return "unknown", "GB"
        return to_unit(used, "GB")

    @property
    def storage_total(self) -> Tuple[str, str]:
        total = self._get_storage_values(_TOTAL)[0]
        if total is None:
            return "unknown", "GB"
        return to_unit(total, "GB")

    @property
    def storage_used_percent(self) -> str:
        used, total = self._get_storage_values(_USED, _TOTAL)
        if used is None or total is None:
            return "unknown"
        try:
            return percent(float(used), float(total))
        except (TypeError, ValueError, ZeroDivisionError):
            return "unknown"

    @property
    def storage_all(self) -> StorageT:
        used, total = self._get_storage_values(_USED, _TOTAL)
        if used is None or total is None:
            return {
                "used_percent": "unknown",
                "used": ("unknown", "GB"),
                "total": ("unknown", "GB"),
            }
        try:
            used_percent = percent(float(used), float(total))
        except (TypeError, ValueError, ZeroDivisionError):
            used_percent = "unknown"
        return {
            "used_percent": used_percent,
            "used": to_unit(used, "GB"),
            "total": to_unit(total, "GB"),
        }
