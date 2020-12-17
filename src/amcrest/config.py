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

# How long to wait for the server send data before giving up, as a float
# or a (connect timeout, read timeout) tuple.
# requests library suggests a value slightly larger than a multiple of 3.
TIMEOUT_HTTP_PROTOCOL = 6.05

# Socket TCP keep alive parameters.
KEEPALIVE_IDLE = 20
KEEPALIVE_INTERVAL = 10
KEEPALIVE_COUNT = 5

# Retries - maximum number of retries each connection should attempt
# Default value from requests library is 3
MAX_RETRY_HTTP_CONNECTION = 3
