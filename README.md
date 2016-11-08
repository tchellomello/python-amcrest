# python-amcrest
This repository is python module for Amcrest SDK HTTP API.

This is a working in process project.

All tests executed with Amcrest IP2M-841B
If you have different model, fell free to contribute.

Installation
============


PIP + GIT
---------

```bash
$ pip install git+https://github.com/tchellomello/python-amcrest
$ eval "$(register-python-argcomplete amcrest-cli)"

To enable amcrest-cli autocomplete in the system:
$ sudo vi /etc/profile.d/amcrest-cli-autocomplete.sh
  eval "$(register-python-argcomplete amcrest-cli)"
```

Usage
=====

Module Examples
---------------

```python
>>> from amcrest import AmcrestCamera

>>> amcrest = AmcrestCamera('192.168.0.1', 80, 'admin', 'password')
>>> camera = amcrest.camera

Check software information
>>> camera.software_information
'version=2.420.AC00.15.R\r\nBuildDate=2016-09-08'

Capture snapshot
>>> camera.snapshot(0, "/home/user/Desktop/snapshot00.jpeg")
<requests.packages.urllib3.response.HTTPResponse object at 0x7f84945083c8>

Capture audio
>>> camera.audio_stream_capture(httptype="singlepart", channel=1, path_file="/home/user/Desktop/audio.aac")
CTRL-C to stop the continuous audio flow or use a timer

Move camera down
>>> camera.ptz_control_command(action="start", code="Down", arg1=0, arg2=0, arg3=0)))

Record realtime stream into a file
>>> camera.realtime_stream(path_file="/home/user/Desktop/myvideo")
CTRL-C to stop the continuous video flow or use a timer
$ mplayer /home/user/Desktop/myvideo


```

Command Line
------------
```bash
$ man amcrest-cli

or

$ amcrest-cli --help
