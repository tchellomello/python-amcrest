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

from amcrest.http import Http
from amcrest.utils import pretty


class Record(Http):
    @property
    def record_capability(self) -> str:
        ret = self.command("recordManager.cgi?action=getCaps")
        return ret.content.decode()

    @property
    def record_config(self) -> str:
        ret = self.command("configManager.cgi?action=getConfig&name=Record")
        return ret.content.decode()

    @record_config.setter
    def record_config(self, rec_opt: str) -> str:
        """
        rec_opt is the Record options listed as example below:

        +----------------------+--------+------------------------------------+
        | ParamName            | Value  |   Description                      |
        +----------------------+--------+------------------------------------+
        | Record[ch].PreRecord |Integer | Range is [0-300]                   |
        |                      |        | Prerecord seconds, 0 no prerecord  |
        |                      |        | ch (Channel number) starts from 0  |
        +----------------------|--------|------------------------------------+
        | Record[ch].          |        | wd (week day)                      |
        | TimeSection[wd][ts]  | string | range is [0-6] (Sun/Sat)           |
        |                      |        |                                    |
        |                      |        | ts (time section) range is [0-23]  |
        |                      |        | time section table index           |
        |                      |        |                                    |
        |                      |        | Format: mas hh:mm:ss-hh:mm:ss      |
        |                      |        | Mask: [0-65535], hh: [0-24],       |
        |                      |        | mm: [0-59], ss: [0-59]             |
        |                      |        | Mask indicate record type by bits: |
        |                      |        | Bit0: regular record               |
        |                      |        | Bit1: motion detection record      |
        |                      |        | Bit2: alarm record                 |
        |                      |        | Bit3: card record                  |
        +----------------------+--------+------------------------------------+

        Example:
        Record[0].TimeSection[0][0]=6 00:00:00-23:59:59


        rec_opt format:
        <paramName>=<paramValue>[&<paramName>=<paramValue>...]
        """

        ret = self.command(f"configManager.cgi?action=setConfig&{rec_opt}")
        return ret.content.decode()

    @property
    def media_global_config(self) -> str:
        ret = self.command(
            "configManager.cgi?action=getConfig&name=MediaGlobal"
        )
        return ret.content.decode()

    def get_record_mode(self, channel: int = 0) -> str:
        status_code = {0: "Automatic", 1: "Manual", 2: "Stop"}

        ret = self.command(
            "configManager.cgi?action=getConfig&name=RecordMode"
        )
        statuses = [
            pretty(s)
            for s in ret.content.decode().split()
            if f"[{channel}].Mode=" in s
        ]
        if len(statuses) != 1:
            return "Unknown"

        status = int(statuses[0])
        if status not in status_code:
            return "Unknown"

        return status_code[status]

    def set_record_mode(self, record_opt: int, *, channel: int = 0) -> str:
        """
        Params:

        channel:
        video index, start from 0

        record_opt:
        +----------------------------+-----------------+-------------------+
        | ParamName                  | ParamValue type | Description       |
        +----------------------------+-----------------+-------------------+
        | RecordMode[channel].Mode   | integer         | Range os {0, 1, 2}|
        |                            |                 | 0: automatically  |
        |                            |                 | 1: manually       |
        |                            |                 | 2: stop record    |
        +----------------------------+-----------------+-------------------+

        record_opt format:
        <paramName>=<paramValue>[&<paramName>=<paramValue>...]
        """
        ret = self.command(
            "configManager.cgi?action=setConfig&RecordMode"
            f"[{channel}].Mode={record_opt}"
        )
        return ret.content.decode()

    @property
    def record_mode(self) -> str:
        return self.get_record_mode()

    @record_mode.setter
    def record_mode(self, record_opt: int) -> None:
        self.set_record_mode(record_opt)
