#!/bin/bash
VIRTUAL_ENV_ROOT=virtualenvs
VENV_NAME=image_manager_py26

rm -rf /opt/letv/image-manager
rm -rf /etc/init.d/image-manager
rm -rf /etc/sysconfig/image-manager
source /opt/${VIRTUAL_ENV_ROOT}/${VENV_NAME}/bin/activate
pip uninstall -y image_manager

exit 0
