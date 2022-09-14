#!/bin/bash

while getopts ":o:w:f:" opt; do
  case $opt in
    o) OPTION="$OPTARG"
    ;;
    w) WEEK="$OPTARG"
    ;;
    f) LEAGUES_FILE="$OPTARG"
    ;;
    \?) echo "Invalid option $OPTARG" >&2
    ;;
  esac
done
ABSPATH=$(cd "$(dirname "$0")"; pwd)
OUTPUT_FOLDER=/tmp/data/
: "${LEAGUES_FILE:=./data/leagues_2022.txt}"

cd $ABSPATH

if [[ ! -e $LEAGUES_FILE ]]; then
  echo "Missing leagues file: $LEAGUES_FILE"
  exit 1
fi

[[ $OPTION == "" ]] && echo "Option (-o) not specified. Valid values are: matchups,users,rosters" && exit 1
[[ $OPTION == "rosters" ]] || [[ $OPTION == "matchups" ]] && [[ $WEEK == "" ]] && echo "Week (-w) not specified." && exit 1

echo "Starting script"

while read league; do
  if [[ $OPTION == "users" ]]; then
      mkdir -p ${OUTPUT_FOLDER}/data/users
      FILENAME=${OUTPUT_FOLDER}/data/users/${league}_users
      if [[ ! -e ${FILENAME}.json ]]; then
          echo "Getting League $league users..."
          curl  https://api.sleeper.app/v1/league/${league}/users -s > ${FILENAME}.json
      fi
      echo "Converting League $league users"
      python ./sleeper_parser.py --file ${FILENAME}.json --option users --league_id $league >> ${OUTPUT_FOLDER}/data/users.csv
      echo "Users CSV: ./data/users.csv"
  fi
  if [[ $OPTION == "rosters" ]]; then
      mkdir -p ${OUTPUT_FOLDER}/data/rosters
      FILENAME=${OUTPUT_FOLDER}/data/rosters/${league}_rosters_week$WEEK
      if [[ ! -e ${FILENAME}.json ]]; then
          echo "Getting League $league rosters..."
          curl  https://api.sleeper.app/v1/league/${league}/rosters -s > ${FILENAME}.json
      fi
      echo "Converting League $league rosters"
      python ./sleeper_parser.py --file ${FILENAME}.json --option roster-ids --league_id $league >> ${OUTPUT_FOLDER}/data/rosters_week$WEEK.csv
      echo "Rosters CSV: ./data/rosters_week$WEEK..csv"
  fi
  if [[ $OPTION == "matchups" ]]; then
      mkdir -p ${OUTPUT_FOLDER}/data/matchups
      FILENAME=${OUTPUT_FOLDER}/data/matchups/${league}_matchups_week${WEEK}
      if [[ ! -e ${FILENAME}.json ]]; then
          echo "Getting League $league matchups..."
          curl  https://api.sleeper.app/v1/league/${league}/matchups/${WEEK} -s > ${FILENAME}.json
      fi
      echo "Converting League $league matchups"
      python ./sleeper_parser.py --file ${FILENAME}.json --rosters ./data/rosters/${league}_rosters_week$WEEK.json --option matchups --league_id $league --week ${WEEK} >> ${OUTPUT_FOLDER}/data/matchups_week${WEEK}.csv
      echo "Matchups CSV: ./data/matchups_week${WEEK}.csv"
    fi
done < "$LEAGUES_FILE"

echo "Done"

exit 0
