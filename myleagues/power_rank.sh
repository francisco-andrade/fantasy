#!/bin/bash

LEAGUES_FILE=./leagues.txt
ABSPATH=$(cd "$(dirname "$0")"; pwd)
cd $ABSPATH

while getopts ":o:w:i:" opt; do
  case $opt in
    o) OPTION="$OPTARG"
    ;;
    w) WEEK="$OPTARG"
    ;;
    i) LEAGUE_ID="$OPTARG"
    ;;
    \?) echo "Invalid option $OPTARG" >&2
    ;;
  esac
done

[[ $OPTION == "" ]] && echo "Option (-o) not specified. Valid values are: users,power" && exit 1
[[ $OPTION == "power" ]] && [[ $WEEK == "" ]] && echo "Week (-w) not specified." && exit 1

print_users(){
  league=$1
  FILENAME=./data/${league}_users
  if [[ ! -e ${FILENAME}.json ]]; then
      curl  https://api.sleeper.app/v1/league/${league}/users -s > ${FILENAME}.json
  fi
  python ./sleeper_parser.py --file ${FILENAME}.json --option users --league_id $league > ./data/users.csv
  cat ./data/users.csv
}

print_power(){
  league=$1
  FILENAME=./data/${league}_rosters_week$WEEK
  if [[ ! -e ${FILENAME}.json ]]; then
      curl  https://api.sleeper.app/v1/league/${league}/rosters -s > ${FILENAME}.json
  fi
  python ./sleeper_parser.py --file ${FILENAME}.json --option power --league_id $league --week $WEEK > ./data/power-rank_week$WEEK.csv
  cat ./data/power-rank_week$WEEK.csv
}

if [[ -n $LEAGUE_ID ]]; then
    if [[ $OPTION == "users" ]]; then
      print_users $LEAGUE_ID
    fi
    if [[ $OPTION == "power" ]]; then
      print_power $LEAGUE_ID
    fi
else
  if [[ ! -e $LEAGUES_FILE ]]; then
    echo "Missing leagues file: $LEAGUES_FILE"
    exit 1
  fi
  while read LEAGUE_ID; do
    if [[ $OPTION == "users" ]]; then
      print_users $LEAGUE_ID
    fi
    if [[ $OPTION == "power" ]]; then
      print_power $league
    fi
  done < "$LEAGUES_FILE"
fi

exit 0
