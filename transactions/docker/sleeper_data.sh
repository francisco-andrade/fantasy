#!/bin/bash

while getopts ":o:w:l:" opt; do
  case $opt in
    o) OPTION="$OPTARG"
    ;;
    w) WEEK="$OPTARG"
    ;;
    l) LEAGUE="$OPTARG"
    ;;
    \?) echo "Invalid option $OPTARG" >&2
    ;;
  esac
done

: "${WEEK:=1}"
: "${FOLDER:=/root/sleeper/}"

[[ -z $LEAGUE ]] && LEAGUES_FILE=./data/leagues.txt
[[ $OPTION == "" ]] && echo "Option (-o) not specified. Valid values are: users,power,transactions" && exit 1


if [[ -z $LEAGUE ]] && [[ ! -e $LEAGUES_FILE ]]; then
  echo "Missing leagues file: $LEAGUES_FILE"
  exit 1
fi

echo "Starting script"

cd $FOLDER

if [[ $OPTION == "transactions" ]]; then
  mkdir -p ./data/transactions
  if [[ -z $LEAGUE ]]; then 
    while read LEAGUE_ID; do
        PLAYERS_FILENAME=./data/transactions/players
        if [[ ! -e ${PLAYERS_FILENAME}.json ]]; then
            echo "Getting all players..."
            curl https://api.sleeper.app/v1/players/nfl -s > ${PLAYERS_FILENAME}.json
        fi
        ROSTERS_FILENAME=./data/transactions/${LEAGUE_ID}_rosters
        if [[ ! -e ${ROSTERS_FILENAME}.json ]]; then
            echo "Getting League $LEAGUE_ID rosters..."
            curl https://api.sleeper.app/v1/league/${LEAGUE_ID}/rosters -s > ${ROSTERS_FILENAME}.json
        fi
        USERS_FILENAME=./data/transactions/${LEAGUE_ID}_users
        if [[ ! -e ${USERS_FILENAME}.json ]]; then
            echo "Getting League $LEAGUE_ID rosters..."
            curl https://api.sleeper.app/v1/league/${LEAGUE_ID}/users -s > ${USERS_FILENAME}.json
        fi
        TRANSACTIONS_FILENAME=./data/transactions/${LEAGUE_ID}_transactions_week${WEEK}
        if [[ ! -e ${TRANSACTIONS_FILENAME}.json ]]; then
            echo "Getting League $LEAGUE_ID transactions..."
            curl https://api.sleeper.app/v1/league/${LEAGUE_ID}/transactions/${WEEK} -s > ${TRANSACTIONS_FILENAME}.json
        fi
        echo "Converting League $LEAGUE_ID transactions"
        python ./sleeper_parser.py --file ${TRANSACTIONS_FILENAME}.json --rosters ${ROSTERS_FILENAME}.json --users ${USERS_FILENAME}.json --players ${PLAYERS_FILENAME}.json --option transactions --league_id $LEAGUE_ID >> ./data/transactions.csv
        echo "Transactions CSV: ./data/transactions.csv"
    done < "$LEAGUES_FILE"
  else
    LEAGUE_ID=$LEAGUE
    PLAYERS_FILENAME=./data/players
    if [[ ! -e ${PLAYERS_FILENAME}.json ]]; then
        echo "Getting all players..."
        curl https://api.sleeper.app/v1/players/nfl -s > ${PLAYERS_FILENAME}.json
    fi
    ROSTERS_FILENAME=./data/transactions/${LEAGUE_ID}_rosters
    if [[ ! -e ${ROSTERS_FILENAME}.json ]]; then
        echo "Getting League $LEAGUE_ID rosters..."
        curl https://api.sleeper.app/v1/league/${LEAGUE_ID}/rosters -s > ${ROSTERS_FILENAME}.json
    fi
    USERS_FILENAME=./data/transactions/${LEAGUE_ID}_users
    if [[ ! -e ${USERS_FILENAME}.json ]]; then
        echo "Getting League $LEAGUE_ID rosters..."
        curl https://api.sleeper.app/v1/league/${LEAGUE_ID}/users -s > ${USERS_FILENAME}.json
    fi
    TRANSACTIONS_FILENAME=./data/transactions/${LEAGUE_ID}_transactions_week${WEEK}
    if [[ ! -e ${TRANSACTIONS_FILENAME}.json ]]; then
        echo "Getting League $LEAGUE_ID transactions..."
        curl https://api.sleeper.app/v1/league/${LEAGUE_ID}/transactions/${WEEK} -s > ${TRANSACTIONS_FILENAME}.json
    fi
    echo "Converting League $LEAGUE_ID transactions"
    python ./sleeper_parser.py --file ${TRANSACTIONS_FILENAME}.json --rosters ${ROSTERS_FILENAME}.json --users ${USERS_FILENAME}.json --players ${PLAYERS_FILENAME}.json --option transactions --league_id $LEAGUE_ID >> ./data/transactions.csv
    echo "Transactions CSV: ./data/transactions.csv"
  fi

  cat ./data/transactions.csv | sort
  rm ./data/transactions.csv
fi

echo "Done"

exit 0
