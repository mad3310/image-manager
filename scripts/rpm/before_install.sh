#!/bin/bash
VIRTUAL_ENV_ROOT=virtualenvs
VENV_NAME=image_manager_py26

cd /opt
mkdir -p $VIRTUAL_ENV_ROOT

cd $VIRTUAL_ENV_ROOT
if [ ! -d $VENV_NAME ]; then
     virtualenv --no-site-packages $VENV_NAME
fi

source ${VENV_NAME}/bin/activate
pip install docker-py==1.8.1
pip install tornado==4.3
pip install futures==3.0.5
pip install boto==2.40.0
pip install kazoo==2.2.1
exit 0
