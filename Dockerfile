FROM python:3.12-alpine3.19

COPY . /tmp/app
RUN pip3 install --no-cache-dir /tmp/app; \
    rm -rf /tmp/app
USER nobody
ENTRYPOINT ["kompozit"]