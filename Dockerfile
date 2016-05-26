FROM frolvlad/alpine-python3

# COPY tasks /opt/www/tasks
# COPY config.py /opt/www/
COPY requirements.txt /opt/www/
WORKDIR /opt/www/


RUN apk add --no-cache --virtual=build_dependencies musl-dev gcc python3-dev libffi-dev && \
    # cd /opt/www && \
    pip install -r requirements.txt && \
    # invoke app.dependencies.install && \
    rm -rf ~/.cache/pip && \
    apk del build_dependencies

COPY app/ /opt/www/

RUN chown -R nobody /opt/www/

USER nobody
CMD [ "./opt/www/app/__init__.py"]
