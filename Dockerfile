FROM jessie-lxc

RUN apt-get update && apt-get install python3 

# COPY tasks /opt/www/tasks
# COPY config.py /opt/www/
COPY requirements.txt /opt/www/

WORKDIR /opt/www/


RUN apt-get install -y python3-pip && pip3 install -r requirements.txt && \
    # invoke app.dependencies.install && \
    rm -rf ~/.cache/pip

WORKDIR /

COPY app/ /opt/www/
COPY entrypoint.sh /opt/www/

RUN chown -R nobody /opt/www/

ENV SERVER_ADDRESS '127.0.0.1'
ENV RABBITMQ_ADDRESS '127.0.0.1'
ENV TARGET 'http://127.0.0.1:8080/peer/doc/random'
ENV WRITERS 10
ENV READERS 10
ENV TYPING_SPEED 5
ENV DURATION 3600


USER nobody
# CMD [ "sh", "/opt/www/entrypoint.sh"]
