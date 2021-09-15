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

[[ $OPTION == "" ]] && echo "Option (-o) not specified. Valid values are: matchups,users,rosters" && exit 1
[[ $OPTION == "matchups" ]] && [[ $WEEK == "" ]] && echo "Week (-w) not specified." && exit 1

echo "Starting script"

while read league; do
  if [[ $OPTION == "users" ]]; then
      FILENAME=./data/users/${league}_users
      if [[ ! -e ${FILENAME}.json ]]; then
          echo "Getting League $league users..."
          curl  https://api.sleeper.app/v1/league/${league}/users -s > ${FILENAME}.json
      fi
      echo "Converting League $league users"
      python ./sleeper_converter.py --file ${FILENAME}.json --option users --league_id $league >> ./data/users.csv
      echo "Users CSV: ./data/users.csv"
  fi
  if [[ $OPTION == "rosters" ]]; then
      FILENAME=./data/rosters/${league}_rosters
      if [[ ! -e ${FILENAME}.json ]]; then
          echo "Getting League $league rosters..."
          curl  https://api.sleeper.app/v1/league/${league}/rosters -s > ${FILENAME}.json
      fi
      echo "Converting League $league rosters"
      python ./sleeper_converter.py --file ${FILENAME}.json --option roster-ids --league_id $league >> ./data/rosters.csv
      echo "Rosters CSV: ./data/rosters.csv"
  fi
  if [[ $OPTION == "matchups" ]]; then
      FILENAME=./data/matchups/${league}_matchups_week${WEEK}
      if [[ ! -e ${FILENAME}.json ]]; then
          echo "Getting League $league matchups..."
          curl  https://api.sleeper.app/v1/league/${league}/matchups/${WEEK} -s > ${FILENAME}.json
      fi
      echo "Converting League $league matchups"
      python ./sleeper_converter.py --file ${FILENAME}.json --option matchups --league_id $league --week ${WEEK} >> ./data/matchups_week${WEEK}.csv
      echo "Matchups CSV: ./data/matchups_week${WEEK}.csv"
    fi
done < "$LEAGUES_FILE"

echo "Done"

exit 0
