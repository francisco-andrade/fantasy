#!/bin/bash

LEAGUES_FILE=./leagues.txt

if [[ ! -e $LEAGUES_FILE ]]; then
  echo "Missing leagues file: $LEAGUES_FILE"
  exit 1
fi

while getopts ":o:w:" opt; do
  case $opt in
    o) OPTION="$OPTARG"
    ;;
    w) WEEK="$OPTARG"
    ;;
    \?) echo "Invalid option $OPTARG" >&2
    ;;
  esac
done

[[ $OPTION == "" ]] && echo "Option (-o) not specified. Valid values are: users,power" && exit 1
[[ $OPTION == "power" ]] && [[ $WEEK == "" ]] && echo "Week (-w) not specified." && exit 1

echo "Starting script"

while read league; do
  if [[ $OPTION == "users" ]]; then
      FILENAME=./data/users/${league}_users
      if [[ ! -e ${FILENAME}.json ]]; then
          echo "Getting League $league users..."
          curl  https://api.sleeper.app/v1/league/${league}/users -s > ${FILENAME}.json
      fi
      echo "Converting League $league users"
      python ./sleeper_parser.py --file ${FILENAME}.json --option users --league_id $league >> ./data/users.csv
      echo "Users CSV: ./data/users.csv"
  fi
  if [[ $OPTION == "power" ]]; then
      FILENAME=./data/rosters/${league}_rosters_week$WEEK
      if [[ ! -e ${FILENAME}.json ]]; then
          echo "Getting League $league rosters..."
          curl  https://api.sleeper.app/v1/league/${league}/rosters -s > ${FILENAME}.json
      fi
      echo "Generating League $league PR"
      python ./sleeper_parser.py --file ${FILENAME}.json --option power --league_id $league --week $WEEK >> ./data/power-rank_week$WEEK.csv
      echo "PR CSV: ./data/power-rank_week$WEEK..csv"
  fi
done < "$LEAGUES_FILE"

echo "Done"

exit 0
