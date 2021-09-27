#!/bin/bash
docker rm -f babyphp1
docker build -t babyphp1 . && \
docker run -d --name=babyphp1 --rm -p1337:80 -it babyphp1