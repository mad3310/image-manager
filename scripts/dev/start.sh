#!/bin/sh
BASE_DIR=$(cd `dirname $0`; pwd)
CODEDIR=${BASE_DIR}/../../
virtualenv=${BASE_DIR}/tmpenv
if [ ! -d $virtualenv ]; then
    virtualenv --no-site-packages ${virtualenv}
fi
source ${virtualenv}/bin/activate
LOGFILE=${BASE_DIR}/config/root.log
log=$(echo "${LOGFILE}" | sed 's/\//\\\//g')
echo $BASE_DIR
echo $CODEDIR
echo $virtualenv
echo $LOGFILE
echo $log

sed '1,$s/^args=.*$/args=("\/home\/liujinliu\/log\/root.log", "a", 10000000, 5)/g' logging.conf
cd $CODEDIR
make uninstall
make install
cd -
image_manager_start --base_dir=${BASE_DIR} --dockerfile_dir=${BASE_DIR}/dockerfile

