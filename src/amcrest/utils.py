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
from datetime import datetime
from typing import List

# pylint: disable=no-name-in-module
from distutils import util
from typing import List, Tuple, Union

DATEFMT = "%Y-%m-%d %H:%M:%S"
PRECISION = 2


def clean_url(url: str) -> str:
    host = re.sub(r"^http[s]?://", "", url, flags=re.IGNORECASE)
    host = re.sub(r"/$", "", host)
    return host


def pretty(value: str, delimiter: str = "=") -> str:
    """Format string key=value."""
    return value.strip().rpartition(delimiter)[2]


def date_to_str(value: datetime) -> str:
    return value.strftime(DATEFMT)


def str_to_date(value: str) -> datetime:
    return datetime.strptime(value, DATEFMT)


def percent(part: float, whole: float) -> str:
    """Convert data to percent"""
    return str(round(100 * part / whole, PRECISION))


def str2bool(value: Union[str, int]) -> bool:
    """
    Args:
        value - text to be converted to boolean
         True values: y, yes, true, t, on, 1
         False values: n, no, false, off, 0
    """
    if isinstance(value, str):
        return bool(util.strtobool(value))
    return bool(value)


def to_unit(
    value: Union[None, str, int, float], unit: str = "B"
) -> Tuple[str, str]:
    """Convert bytes to give unit."""
    byte_array = ["B", "KB", "MB", "GB", "TB"]

    if unit not in byte_array:
        raise ValueError(f"Unit {unit} missing from known units")

    if value is None:
        return "unknown", unit
    if isinstance(value, (int, float)):
        value_f = value
    else:
        try:
            value_f = float(value)
        except (TypeError, ValueError):
            return "unknown", unit

    result = value_f / 1024 ** byte_array.index(unit)
    return str(round(result, PRECISION)), unit


def extract_audio_video_enabled(param: str, resp: str) -> List[bool]:
    """Extract if any audio/video stream enabled from response."""
    parts = [
        part.rpartition("=")[2] == "true"
        for part in resp.split()
        if f".{param}Enable=" in part
    ]
    return parts


def enable_audio_video_cmd(
    param: str, enable: bool, channel: int, *, stream: str
) -> str:
    """Return command to enable/disable all audio/video streams."""
    formats = [("Extra", 3), ("Main", 4)]
    if param == "Video":
        formats.append(("Snap", 3))

    if stream is not None:
        formats = [x for x in formats if x[0] == stream]
        if not formats:
            raise RuntimeError(f"Bad stream specified: {stream}")

    set_enable = str(enable).lower()
    cmds = ["configManager.cgi?action=setConfig"]
    cmds.extend(
        f"Encode[{channel}].{fmt}Format[{i}].{param}Enable={set_enable}"
        for fmt, num in formats
        for i in range(num)
    )
    return "&".join(cmds)
