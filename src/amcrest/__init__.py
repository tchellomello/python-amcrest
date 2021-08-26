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
from .audio import Audio
from .event import Event
from .exceptions import AmcrestError, CommError, LoginError  # noqa: F401
from .log import Log
from .media import Media
from .motion_detection import MotionDetection
from .nas import Nas
from .network import Network
from .ptz import Ptz
from .record import Record
from .snapshot import Snapshot
from .special import Special
from .storage import Storage
from .system import System
from .user_management import UserManagement
from .video import Video
from .privacy_mode import PrivacyMode


class AmcrestCamera:
    """Amcrest camera object implementation."""

    def __init__(
        self,
        host,
        port,
        user,
        password,
        *,
        verbose=True,
        protocol="http",
        ssl_verify=True,
        retries_connection=None,
        timeout_protocol=None,
    ) -> None:
        super().__init__()
        self.camera = ApiWrapper(
            host=host,
            port=port,
            user=user,
            password=password,
            verbose=verbose,
            protocol=protocol,
            ssl_verify=ssl_verify,
            retries_connection=retries_connection,
            timeout_protocol=timeout_protocol,
        )


# pylint: disable=too-many-ancestors
class ApiWrapper(
    System,
    Network,
    MotionDetection,
    Snapshot,
    UserManagement,
    Event,
    Audio,
    Record,
    Video,
    Log,
    Ptz,
    Special,
    Storage,
    Nas,
    Media,
    PrivacyMode,
):
    pass
