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
cd /opt/letv/image-manager/packages
pip install ordereddict-1.1.tar.gz
pip install backports.ssl_match_hostname-3.5.0.1.tar.gz
pip install argparse-1.4.0-py2.py3-none-any.whl
pip install backports_abc-0.4-py2.py3-none-any.whl
pip install ipaddress-1.0.16-py27-none-any.whl
pip install six-1.10.0-py2.py3-none-any.whl
pip install singledispatch-3.4.0.3-py2.py3-none-any.whl
pip install requests-2.10.0-py2.py3-none-any.whl
pip install futures-3.0.5-py2-none-any.whl
pip install boto-2.40.0-py2.py3-none-any.whl
pip install websocket_client-0.37.0.tar.gz 
pip install docker_py-1.8.1-py2.py3-none-any.whl
pip install kazoo-2.2.1-py2.py3-none-any.whl
pip install tornado-4.3-cp35-none-win_amd64.whl
exit 0
