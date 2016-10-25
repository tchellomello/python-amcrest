# python-amcrest
This repository is a wapper for Amcrest SDK HTTP API.

This is a working in process project.

Installation
============


PIP + GIT
---------

```bash
$ pip install git+https://github.com/tchellomello/python-amcrest
```

Usage
=====

Module
------

```python
from amcrest import AmcrestCamera

c = AmcrestCamera('192.168.0.1', 80, 'admin', 'password')

c.is_motion_detection_enabled()
True

c.enable_motion_detection()
True

c.disable_motion_detection()
True
```

Command Line
------------
```bash
$ amcrest-cli --help
usage: amcrest-cli [-h] -H HOSTNAME -u USERNAME -p PASSWORD [-P PORT]
                   [--get-snapshot [SNAPSHOT_OPTION]] [--get-current-time]
                   [--motion-detection-status] [--enable-motion-detection]
                   [--disable-motion-detection] [--output OUTPUT]

Command line interface for Amcrest cameras.

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        hostname or ip address for Amcrest camera
  -u USERNAME, --username USERNAME
                        username for Amcrest camera
  -p PASSWORD, --password PASSWORD
                        password for Amcrest camera
  -P PORT, --port PORT  port to Amcrest camera. Default: 80
  --get-snapshot [SNAPSHOT_OPTION]
                        get snapshot, use 0, 1 or 2
                        0 - regular snapshot
                        1 - motion detection snapshot
                        2 - alarm snapshot
  --get-current-time    Get camera current time
  --motion-detection-status
                        Return motion detection status.
  --enable-motion-detection
                        Enable motion detection.
  --disable-motion-detection
                        Disable motion detection.
  --output OUTPUT       output file name

### getting snapshot from camera
$ amcrest-cli -H <IP> -u <user> -p <password> --get-snapshot --output ~/Desktop/snapshot.jpg
```
