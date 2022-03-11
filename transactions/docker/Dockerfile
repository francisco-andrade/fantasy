# B2W-Freight-Extractor

FROM centos:centos7
MAINTAINER Francisco fjandrade15@gmail.com

RUN mkdir -p /root/sleeper/data/

COPY sleeper_data.sh /root/sleeper/
COPY sleeper_parser.py /root/sleeper/
COPY ./data/leagues.txt /root/sleeper/data/
COPY ./data/players.json /root/sleeper/data/

# Configure default container command
ENTRYPOINT ["/root/sleeper/sleeper_data.sh"]

