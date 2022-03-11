#!/usr/bin/python
# python ./sleeper_converter.py --option players --file file.json --output csv
from __future__ import division
import sys
import json
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="transactions file path")
parser.add_argument("--rosters", help="rosters file path")
parser.add_argument("--users", help="users file path")
parser.add_argument("--players", help="players file path")
parser.add_argument("--option", help="options: transactions", default="transactions")
parser.add_argument("--output", help="outputs: csv", default="csv")
parser.add_argument("--league_id", help="league_id", default="1")
parser.add_argument("--week", help="week", default="1")
args = parser.parse_args()

def get_owner(data, roster_id):
    for item in data:
        if str(roster_id) == str(item['roster_id']):
            return item['owner_id']

def get_user(data, user_id):
    for item in data:
        if user_id is None:
            return "Unknown"
        else:
            if str(user_id) == str(item['user_id']):
                if 'team_name' in item['metadata']:
                    return item['metadata']['team_name']
                else:
                    return str(item['display_name'])

def print_transactions(data, rosters, users, players):
    try:
        for item in data:
            if str(item['status']) == 'complete':
                # notes = check_value(item['metadata'], 'notes', 'None')
                if bool(item['adds']):
                    for adds_key in item['adds'].keys():
                        adds_value = item['adds'][adds_key]
                        adds_player_name = players.get(str(adds_key))['first_name'] + " " + players.get(str(adds_key))['last_name']
                        bid = "0"
                        if item['settings'] is None:
                            bid = "0"
                        else:
                            if 'waiver_bid' in item['settings']:
                                bid = item['settings']['waiver_bid']
                            else:
                                bid = "0"
                        adds_positions = ""
                        for adds_position in players.get(str(adds_key))['fantasy_positions']:
                            adds_positions += str(adds_position) + "/"
                        print(time.strftime("%y/%m/%d %H:%M:%S", time.localtime(item['created']/1000)) + ";" + str(args.league_id) + ";add;" + str(item['type']) + ";" + str(item['status']) + ";" + get_user(users, get_owner(rosters, adds_value)) + ";" + adds_player_name + ";" + adds_positions[:-1] + ";" + str(bid))
                if bool(item['drops']):
                    for drops_key in item['drops'].keys():
                        drops_value = item['drops'][drops_key]
                        drops_player_name = players.get(str(drops_key))['first_name'] + " " + players.get(str(drops_key))['last_name']
                        bid = "0"
                        drops_positions = ""
                        for drops_position in players.get(str(drops_key))['fantasy_positions']:
                            drops_positions += str(drops_position) + "/"                        
                        print(time.strftime("%y/%m/%d %H:%M:%S", time.localtime(item['created']/1000)) + ";" + str(args.league_id) + ";drop;" + str(item['type']) + ";" + str(item['status']) + ";" + get_user(users, get_owner(rosters, drops_value)) + ";" + drops_player_name + ";" + drops_positions[:-1] + ";" + bid)
    except Exception as e:
        raise

try:
    with open(args.file) as transactions_file:
        data = json.load(transactions_file)
        if args.option == "transactions":
            with open(args.players) as players_file:
                players = json.load(players_file)
                with open(args.rosters) as rosters_file:
                    rosters = json.load(rosters_file)
                    with open(args.users) as users_file:
                        users = json.load(users_file)
                        print_transactions(data, rosters, users, players)
except Exception as e:
    print(str(e))
