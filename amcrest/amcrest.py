# -*- coding: utf-8 -*-
# vim:sw=4:ts=4:et

try:
    import json
except:
    import simplejson as json

import requests
from requests.auth import HTTPBasicAuth

class AmcrestCamera(object):
    """Amcrest camera object implementation."""

    def __init__(self, host, port, user, password, verbose=True,
            protocol='http'):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._verbose = verbose
        self._protocol = protocol
        self._token = HTTPBasicAuth(self._user, self._password)


    def base_url(self, param=""):
        return '%s://%s:%s/cgi-bin/%s' %(self._protocol, self._host,
                                                str(self._port), param)

    def command(self, cmd):
        try:
            url = self.base_url(cmd)
            resp = requests.get(url, auth=self._token)
        except:
            raise

        #data = json.dumps(resp.content.decode('utf-8'))
        data = resp.content.decode('utf-8')
        return data

    @property
    def get_current_time(self):
        arg = 'global.cgi?action=getCurrentTime'
        return self.command(arg)

    @property
    def get_video_color_config(self):
        arg = 'configManager.cgi?action=getConfig&name=VideoColor'
        return self.command(arg)

    def is_motion_detection_enabled(self):
        arg = 'configManager.cgi?action=getConfig&name=MotionDetect'
        ret = self.command(arg)
        status = ret.splitlines()[0].split('=')[-1]
        if status == 'true':
            return True
        else:
            return False

    def enable_motion(self):
        arg = 'configManager.cgi?action=setConfig&MotionDetect\[0\].Enable=true'
        ret = self.command(arg)
        if ret == 'OK':
            return True
        else:
            return False

    def disable_motion(self):
        arg = 'configManager.cgi?action=setConfig&MotionDetect\[0\].Enable=false'
        ret = self.command(arg)
        if ret == 'OK':
            return True
        else:
            return False
