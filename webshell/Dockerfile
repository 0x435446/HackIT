FROM alpine:latest


# Install system packages
RUN apk add --no-cache --update \
    python3 py3-pip
RUN pip3 install --no-cache-dir flask 

# Setup user
RUN mkdir -p ~/ReadMe/ReadMe/
RUN mkdir -p /www/challenge

# Expose the port nginx is listening on
EXPOSE 5000

COPY ReadMe /home/webshell/ReadMe/ReadMe/
COPY challenge /www/challenge


RUN adduser webshell -D -u 1000 -g 1000 -s /bin/sh www
USER webshell
RUN whoami






WORKDIR /www/challenge 

#RUN flask run --host=0.0.0.0 

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
