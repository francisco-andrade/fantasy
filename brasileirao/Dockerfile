# Sleeper Brasileirao

FROM centos:centos7
MAINTAINER Francisco fjandrade15@gmail.com

RUN mkdir -p /root/sleeper/data/rosters/

COPY sleeper_tool.sh /root/sleeper/
COPY sleeper_parser.py /root/sleeper/
COPY data/leagues* /root/sleeper/data/
#COPY ./data/players.json /root/sleeper/data/

WORKDIR "/root/sleeper/"

# Configure default container command
# ./sleeper_parser.py --option matchups --league_id 870106348254326784 --week 1
ENTRYPOINT ["/usr/bin/python"]
