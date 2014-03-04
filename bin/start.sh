#!/bin/sh

SCRIPTDIR=$(dirname $0)
cd $SCRIPTDIR/../app

twistd -n --logfile=../log/twistd.log --pidfile=../run/twistd.pid -y app.py
