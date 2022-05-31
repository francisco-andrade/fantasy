#!/bin/bash

ABSPATH=$(cd "$(dirname "$0")"; pwd)

while getopts ":n:d:y:" opt; do
  case $opt in
    n) LEAGUE_NAME="$OPTARG"
    ;;
    d) DRAFT_ID="$OPTARG"
    ;;
    y) YEAR="$OPTARG"
    ;;
    \?) echo "Invalid option $OPTARG" >&2
    ;;
  esac
done

echo "Starting script"
cd $ABSPATH
mkdir -p ./data/

if [[ -n $DRAFT_ID ]]; then
  if [[ ! -e ./data/draft_${YEAR}_${LEAGUE_NAME}.json ]]; then
    curl "https://api.sleeper.app/v1/draft/$DRAFT_ID/picks" > ./data/draft_${YEAR}_${LEAGUE_NAME}.json
  fi
fi

if [[ ! -e ./data/draft_${YEAR}_${LEAGUE_NAME}.csv ]]; then
  python ./sleeper_parser.py --file ./data/draft_${YEAR}_${LEAGUE_NAME}.json --option draft --league_name ${LEAGUE_NAME} >> ./data/draft_${YEAR}_${LEAGUE_NAME}.csv
fi

cat ./data/draft_${YEAR}_${LEAGUE_NAME}.csv

echo "Done"

exit 0
