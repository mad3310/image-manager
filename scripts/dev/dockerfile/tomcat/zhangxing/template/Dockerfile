FROM {REPOSITORY_ADDR}/letv_gce/jdk1.7_tomcat:0.0.1
MAINTAINER liujinliu <liujinliu@letv.com>

USER root

ENV APP_NAME  {APP_NAME}

RUN mkdir -p /letv/deployment

ADD ./files/start_app.sh /letv/start_app.sh

ADD ./files/{APPFILE_NAME} /letv/deployment/{APPFILE_NAME}
#RUN unzip /letv/deployment/{APPFILE_NAME} -d /letv/deployment/
#RUN chown 644 /letv/deployment/{APPFILE_NAME} -R
RUN sed -i 's/example/'$APP_NAME'/g' /letv/server/tomcat_8080/conf/server.xml

ENTRYPOINT /usr/local/init_docker/entrypoint_init.sh && source /usr/local/init_env.sh && sh /letv/start_app.sh && /bin/bash
