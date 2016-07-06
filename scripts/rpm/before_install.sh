#!/bin/bash
VIRTUAL_ENV_ROOT=virtualenvs
VENV_NAME=image_manager_py26

cd /opt
mkdir -p $VIRTUAL_ENV_ROOT

cd $VIRTUAL_ENV_ROOT
if [ ! -d $VENV_NAME ]; then
     virtualenv --no-site-packages --no-pip --no-setuptools --no-wheel $VENV_NAME
fi

#source ${VENV_NAME}/bin/activate
exit 0
