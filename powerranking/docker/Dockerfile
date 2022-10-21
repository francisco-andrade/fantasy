# Sleeper Power Ranking

FROM centos:centos7
MAINTAINER Francisco fjandrade15@gmail.com

RUN mkdir -p /root/sleeper/data/

COPY sleeper_data.py /root/sleeper/
COPY ./data/leagues.txt /root/sleeper/data/

WORKDIR "/root/sleeper/"

# Configure default container command
ENTRYPOINT ["/usr/bin/python"]
