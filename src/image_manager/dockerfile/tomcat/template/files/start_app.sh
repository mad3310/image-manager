#!/bin/bash

#start_app
chown 644 /letv/deployment/$APP_NAME -R

/etc/init.d/tomcat_8080 start
