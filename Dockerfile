FROM quentinlc/jessie-lxc:latest

MAINTAINER Quent Laporte-Chabasse

COPY scripts/requirements.txt /opt/www/

COPY scripts/server /etc/init.d/
RUN chmod 0755 /etc/init.d/server

RUN rm /lib/init/init-d-script
COPY scripts/init-d-script /lib/init/

# Install dependencies
RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  ntp && \
  pip3 install -r /opt/www/requirements.txt && \
  rm -rf ~/.cache/pip

# Copy the entire application
COPY app/ /opt/www/
RUN chown -R nobody /opt/www/

# Set default values
ENV SERVER_ADDRESS '127.0.0.1'
ENV RABBITMQ_ADDRESS '127.0.0.1'
ENV TARGET 'http://127.0.0.1:8080/peer/doc/random'
ENV WRITERS 10
ENV READERS 10
ENV TYPING_SPEED 5
ENV DURATION 3600


CMD [ "sh", "/opt/www/entrypoint.sh"]
