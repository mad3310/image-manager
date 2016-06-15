#!/bin/bash

VIRTUAL_ENV_ROOT=virtualenvs
VENV_NAME=image_manager_py26

source /opt/${VIRTUAL_ENV_ROOT}/${VENV_NAME}/bin/activate
cd /opt/letv/image-manager && pip install *.whl

chmod +x /etc/init.d/image-manager
chkconfig --add image-manager
#/etc/init.d/image-manager start | stop | restart

exit 0
