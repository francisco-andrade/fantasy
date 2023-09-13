#!/bin/bash

while getopts ":o:w:f:l:" opt; do
  case $opt in
    o) OPTION="$OPTARG"
    ;;
    w) WEEK="$OPTARG"
    ;;
    f) LEAGUES_FILE="$OPTARG"
    ;;
    l) LEAGUES="$OPTARG"
    ;;
    \?) echo "Invalid option $OPTARG" >&2
    ;;
  esac
done
ABSPATH=$(cd "$(dirname "$0")"; pwd)
OUTPUT_FOLDER=/tmp
: "${LEAGUES_FILE:=./data/leagues_2022.txt}"

cd $ABSPATH

if [[ ! -e $LEAGUES_FILE ]]; then
  echo "Missing leagues file: $LEAGUES_FILE"
  exit 1
fi

[[ $OPTION == "" ]] && echo "Option (-o) not specified. Valid values are: matchups,users,rosters" && exit 1
[[ $OPTION == "matchups" ]] && [[ $WEEK == "" ]] && echo "Week (-w) not specified." && exit 1

process_league() {
  if [[ $OPTION == "matchups" ]]; then
      mkdir -p ${OUTPUT_FOLDER}/data/rosters ${OUTPUT_FOLDER}/data/matchups
      ROSTERS_FILENAME=${OUTPUT_FOLDER}/data/rosters/${league}_rosters_week${WEEK}.json
      if [[ ! -e ${ROSTERS_FILENAME} ]]; then
          curl  https://api.sleeper.app/v1/league/${league}/rosters -s > ${ROSTERS_FILENAME}
      fi
      MATCHUPS_FILENAME=${OUTPUT_FOLDER}/data/matchups/${league}_matchups_week${WEEK}.json
      if [[ ! -e ${MATCHUPS_FILENAME} ]]; then
          curl  https://api.sleeper.app/v1/league/${league}/matchups/${WEEK} -s > ${MATCHUPS_FILENAME}
      fi
      python ./sleeper_parser.py --file ${MATCHUPS_FILENAME} --rosters ${ROSTERS_FILENAME} --option matchups --league_id $league --week ${WEEK}
    fi
}

if [[ $OPTION == "users" ]]; then
    mkdir -p ${OUTPUT_FOLDER}/data/users
    FILENAME=${OUTPUT_FOLDER}/data/users/${league}_users
    if [[ ! -e ${FILENAME}.json ]]; then
        curl  https://api.sleeper.app/v1/league/${league}/users -s > ${FILENAME}.json
    fi
    python ./sleeper_parser.py --file ${FILENAME}.json --option users --league_id $league
else
  if [[ -n $LEAGUES ]]; then
    echo "week;league_id;roster_id;owner;matchup_id;points;wins;loses;ties;fpts"
    for league in $LEAGUES; do
      process_league $league
    done
  else
    while read league; do
      process_league $league
    done < "$LEAGUES_FILE"
  fi
fi

exit 0
