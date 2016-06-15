FROM 10.160.140.32:5000/dianshang/dlyl_jdk1.7_tomcat:0.0.1
MAINTAINER zhangxing <zhangxing@letv.com>

USER root

ENV APP_NAME tethys_1.0.0.1

ADD ./files/start_app.sh /tmp/start_app.sh

RUN wget -P /letv/deployment/ http://ops.lemall.com/download/india_code/test/$APP_NAME.zip

RUN unzip /letv/deployment/$APP_NAME.zip -d /letv/deployment/

RUN sed -i 's/example/'$APP_NAME'/g' /letv/server/tomcat_8080/conf/server.xml

ENTRYPOINT bash /tmp/init_docker/entrypoint_init.sh && source /tmp/init_env.sh && sh /tmp/start_app.sh  && /bin/bash