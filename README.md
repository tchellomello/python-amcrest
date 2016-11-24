# python-amcrest
This repository is python module for Amcrest SDK HTTP API.

This is a working in process project.

Tests executed with the following Amcrest models:
    IPM-721S
    IP2M-841B

If you have different model, fell free to contribute.

## Installation

- PIP

```bash
$ pip install amcrest
$ eval "$(register-python-argcomplete amcrest-cli)"
```

* To enable amcrest-cli autocomplete in the system:
```bash
$ echo 'eval "$(register-python-argcomplete amcrest-cli)"' >  /etc/profile.d/amcrest-cli-autocomplete.sh
```

- RPM
```bash
$ git clone git@github.com:tchellomello/python-amcrest.git
$ ./autogen.sh
$ make rpm
$ dnf/yum install amcrest-cli-NVR.rpm pythonX-amcrest-NVR.rpm
```

## Usage

- Module

```python
>>> from amcrest import AmcrestCamera

>>> amcrest = AmcrestCamera('192.168.0.1', 80, 'admin', 'password')
>>> camera = amcrest.camera

#Check software information
>>> camera.software_information
'version=2.420.AC00.15.R\r\nBuildDate=2016-09-08'

#Capture snapshot
>>> camera.snapshot(0, "/home/user/Desktop/snapshot00.jpeg")
<requests.packages.urllib3.response.HTTPResponse object at 0x7f84945083c8>

#Capture audio
>>> camera.audio_stream_capture(httptype="singlepart", channel=1, path_file="/home/user/Desktop/audio.aac")
CTRL-C to stop the continuous audio flow or use a timer

#Move camera down
>>> camera.ptz_control_command(action="start", code="Down", arg1=0, arg2=0, arg3=0)))

#Record realtime stream into a file
>>> camera.realtime_stream(path_file="/home/user/Desktop/myvideo")
CTRL-C to stop the continuous video flow or use a timer
$ mplayer /home/user/Desktop/myvideo
```

- Command Line
```bash
$ man amcrest-cli
or
$ amcrest-cli --help
```

* Saving credentials to file.
```bash
$ vim ~/.config/amcrest.conf
[patio]
hostname: 192.168.0.20
username: admin
password: 123456
port: 80

[living_room]
hostname: 192.168.0.21
username: admin
password: secret
port: 80

$ amcrest-cli --camera living_room --version-http-api
version=1.40
```
