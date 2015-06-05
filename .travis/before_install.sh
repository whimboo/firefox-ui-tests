#!/bin/bash
set -ev

if [ "$TRAVIS_OS_NAME" == "linux" ]; then
    /sbin/start-stop-daemon --start --quiet --make-pidfile --pidfile /tmp/custom_xvfb_99.pid \
         --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1280x1024x16

    sudo apt-get update -qq
    sudo apt-get install python-pip python-virtualenv
fi
