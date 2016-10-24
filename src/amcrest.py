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

try:
    import json
except:
    import simplejson as json  # noqa

import requests
from requests.auth import HTTPBasicAuth


class AmcrestCamera(object):
    """Amcrest camera object implementation."""

    def __init__(self, host, port, user,
                 password, verbose=True, protocol='http'):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._verbose = verbose
        self._protocol = protocol
        self._token = HTTPBasicAuth(self._user, self._password)

    def base_url(self, param=""):
        return '%s://%s:%s/cgi-bin/%s' % (self._protocol, self._host,
                                          str(self._port), param)

    def command(self, cmd):
        try:
            url = self.base_url(cmd)
            resp = requests.get(url, auth=self._token)
            resp.raise_for_status()
        except:
            raise

        data = resp.content.decode('utf-8')
        return data

    def get_current_time(self):
        return self.command('global.cgi?action=getCurrentTime')

    def is_motion_detection_enabled(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=MotionDetect'
        )

        status = ret.splitlines()[0].split('=')[-1]
        if status == 'true':
            return True

        return False

    def enable_motion_detection(self):
        ret = self.command(
            'configManager.cgi?action=setConfig&MotionDetect[0].Enable=true'
        )

        if "ok" in ret.lower():
            return True

        return False

    def disable_motion_detection(self):
        ret = self.command(
            'configManager.cgi?action=setConfig&MotionDetect[0].Enable=false'
        )

        if "ok" in ret.lower():
            return True

        return False
