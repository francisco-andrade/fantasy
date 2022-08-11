# B2W-Freight-Extractor

FROM centos:centos7
MAINTAINER Francisco fjandrade15@gmail.com

RUN mkdir -p /root/sleeper/data/rosters/

COPY power_rank.sh /root/sleeper/
COPY sleeper_parser.py /root/sleeper/
COPY ./data/users.csv /root/sleeper/data/
COPY ./leagues.txt /root/sleeper/

# Configure default container command
ENTRYPOINT ["/root/sleeper/power_rank.sh"]

