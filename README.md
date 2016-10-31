# python-amcrest
This repository is a wapper for Amcrest SDK HTTP API.

This is a working in process project.

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

Module
------

```python
from amcrest import AmcrestCamera

amcrest = AmcrestCamera('192.168.0.1', 80, 'admin', 'password')
camera = amcrest.camera

camera.is_motion_detection_enabled()
True

camera.enable_motion_detection()
True

camera.disable_motion_detection()
True
```

Command Line
------------
```bash
$ man amcrest-cli

or

$ amcrest-cli --help
