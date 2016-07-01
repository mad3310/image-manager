FROM {REPOSITORY_ADDR}/letv_gce/jdk1.7_resin:0.0.1
MAINTAINER liujinliu <liujinliu@letv.com>

USER root

ENV APP_NAME  {APP_NAME}

RUN mkdir -p /letv/deployment

ADD ./files/start_app.sh /letv/start_app.sh

ADD ./files/{APPFILE_NAME} /letv/deployment/{APPFILE_NAME}

ENTRYPOINT /usr/local/init_docker/entrypoint_init.sh && source /usr/local/init_env.sh && sh /letv/start_app.sh && /bin/bash
