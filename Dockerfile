FROM quentinlc/jessie-lxc:latest

MAINTAINER Quent Laporte-Chabasse
RUN apt-get update && apt-get install python3

# COPY tasks /opt/www/tasks
# COPY config.py /opt/www/
COPY requirements.txt /opt/www/
COPY server /etc/init.d/
RUN chmod 0755 /etc/init.d/server
RUN rm /lib/init/init-d-script
COPY init-d-script /lib/init/

RUN apt-get install -y python3-pip && pip3 install -r /opt/www/requirements.txt && \
    rm -rf ~/.cache/pip

COPY app/ /opt/www/

RUN chown -R nobody /opt/www/

ENV SERVER_ADDRESS '127.0.0.1'
ENV RABBITMQ_ADDRESS '127.0.0.1'
ENV TARGET 'http://127.0.0.1:8080/peer/doc/random'
ENV WRITERS 10
ENV READERS 10
ENV TYPING_SPEED 5
ENV DURATION 3600


CMD [ "sh", "/opt/www/entrypoint.sh"]
