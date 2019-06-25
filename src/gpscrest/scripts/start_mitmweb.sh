#!/bin/bash

# start code proxy
mitmweb --showhost --web-port 9091 --listen-port 9090  --web-open-browser &

# firefox factory proxy
mitmweb --showhost --web-port 8081 --listen-port 8080 --web-open-browser &
