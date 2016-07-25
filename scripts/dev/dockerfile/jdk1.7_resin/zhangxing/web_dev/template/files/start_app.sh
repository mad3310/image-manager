#!/bin/bash

#start_app
chown 644 /letv/deployment/$APP_NAME -R

sh /letv/server/resin/bin/resin.sh -server $APP_NAME start

