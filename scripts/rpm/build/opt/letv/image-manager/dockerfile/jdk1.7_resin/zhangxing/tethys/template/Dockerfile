FROM 192.168.211.131:5000/letv
MAINTAINER zhangxing <zhangxing@letv.com>

USER root

ENV APP_NAME {APP_NAME} 

ADD ./files/start_app.sh /tmp/start_app.sh

#RUN wget -P /letv/deployment/ http://ops.lemall.com/download/india_code/test/$APP_NAME.zip

#RUN unzip /letv/deployment/$APP_NAME.zip -d /letv/deployment/

#RUN sed -i 's/example/'$APP_NAME'/g' /letv/server/resin/conf/resin.xml

ENTRYPOINT bash /tmp/init_docker/entrypoint_init.sh && source /tmp/init_env.sh && sh /tmp/start_app.sh && /bin/bash
ENTRYPOINT /bin/bash
