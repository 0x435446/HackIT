#!/bin/bash
docker build -t webshell .
#docker run --name=webshell --rm -p1338:80 -it webshell
docker run -d -p $1:5000 webshell
