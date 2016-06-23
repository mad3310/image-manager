FROM {REPOSITORY_ADDR}/letv_gce/jdk1.7_resin
MAINTAINER zhangxing <zhangxing@letv.com>

USER root

ENV APP_NAME  {APP_NAME}

ADD ./files/start_app.sh /tmp/start_app.sh

RUN mkdir -p /letv/deployment

ADD ./files/{APPFILE_NAME} /letv/deployment/{APPFILE_NAME}

RUN unzip /letv/deployment/{APP_NAME} -d /letv/deployment/

RUN sed -i 's/example/'{APP_NAME}'/g' /letv/server/resin/conf/resin.xml

#ENTRYPOINT bash /tmp/init_docker/entrypoint_init.sh && source /tmp/init_env.sh && sh /tmp/start_app.sh && /bin/bash
ENTRYPOINT /bin/bash
