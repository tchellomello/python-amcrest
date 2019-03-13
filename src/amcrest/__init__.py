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
from .exceptions import AmcrestError, CommError, LoginError  # noqa: F401
from .http import Http


class AmcrestCamera(object):
    """Amcrest camera object implementation."""

    def __init__(self, host, port, user,
                 password, verbose=True, protocol='http',
                 retries_connection=None, timeout_protocol=None):
        super(AmcrestCamera, self).__init__()
        self.camera = Http(
            host=host,
            port=port,
            user=user,
            password=password,
            verbose=verbose,
            protocol=protocol,
            retries_connection=retries_connection,
            timeout_protocol=timeout_protocol
        )
