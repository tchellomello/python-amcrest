# python-amcrest
This repository is a wapper for Amcrest SDK HTTP API.

This is a working in process project.

```python
from amcrest import AmcrestCamera
c = AmcrestCamera('192.168.0.1', 80, 'admin', 'password')

c.is_motion_detection_enabled()
True

c.enable_motion()
True
```
