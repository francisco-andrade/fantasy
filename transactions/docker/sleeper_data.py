#!/usr/bin/python
# python ./sleeper_data.py --league_id 840062462177955840 --week 1
from __future__ import division
import sys
import json
import argparse
import time
import urllib2
from os.path import exists

parser = argparse.ArgumentParser()
parser.add_argument("--league_id", help="league_id", default="1")
parser.add_argument("--week", help="week", default="1")
parser.add_argument("--debug", help="debug", default="true")
args = parser.parse_args()

def get_owner_id(data, roster_id):
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
                    return item['display_name']

def print_transactions(data, rosters, users, players):
    try:
        transactions_filename = "./transactions_" + args.league_id + "_" + args.week + ".csv"
        with open(transactions_filename, "w") as file_object:
            for item in data:
                if str(item['status']) == 'complete':
                    if bool(item['adds']):
                        for adds_key in item['adds'].keys():
                            adds_value = item['adds'][adds_key]
                            adds_player_name = "Unknown"
                            adds_positions = "Unknown"
                            if str(adds_key) in players:
                                adds_player_name = players.get(str(adds_key))['first_name'] + " " + players.get(str(adds_key))['last_name']
                                adds_positions = ""
                                for adds_position in players.get(str(adds_key))['fantasy_positions']:
                                    adds_positions += str(adds_position) + "/"
                            bid = "0"
                            if item['settings'] is None:
                                bid = "0"
                            else:
                                if 'waiver_bid' in item['settings']:
                                    bid = item['settings']['waiver_bid']
                                else:
                                    bid = "0"
                            team_name = get_user(users, get_owner_id(rosters, adds_value))
                            if args.debug == "false":
                                print(time.strftime("%y/%m/%d %H:%M:%S", time.localtime(item['created']/1000)) + ";" + str(args.league_id) + ";add;" + str(item['type']) + ";" + str(item['status']) + ";" + team_name.encode('utf-8').strip() + ";" + adds_player_name.encode('utf-8').strip() + ";" + adds_positions[:-1] + ";" + str(bid))
                            file_object.write(time.strftime("%y/%m/%d %H:%M:%S", time.localtime(item['created']/1000)) + ";" + str(args.league_id) + ";add;" + str(item['type']) + ";" + str(item['status']) + ";" + team_name.encode('utf-8').strip() + ";" + adds_player_name.encode('utf-8').strip() + ";" + adds_positions[:-1] + ";" + str(bid) + "\n")
                    if bool(item['drops']):
                        for drops_key in item['drops'].keys():
                            drops_value = item['drops'][drops_key]
                            # Player doesnt exist!? ID 8368
                            drops_player_name = "Unknown"
                            drops_positions = "Unknown"
                            if str(drops_key) in players:
                                drops_player_name = players.get(str(drops_key))['first_name'] + " " + players.get(str(drops_key))['last_name']
                                drops_positions = ""
                                for drops_position in players.get(str(drops_key))['fantasy_positions']:
                                    drops_positions += str(drops_position) + "/"
                            bid = "0"
                            team_name = get_user(users, get_owner_id(rosters, drops_value))
                            if args.debug == "false":
                                print(time.strftime("%y/%m/%d %H:%M:%S", time.localtime(item['created']/1000)) + ";" + str(args.league_id) + ";drop;" + str(item['type']) + ";" + str(item['status']) + ";" + team_name.encode('utf-8').strip() + ";" + drops_player_name.encode('utf-8').strip() + ";" + drops_positions[:-1] + ";" + str(bid))
                            file_object.write(time.strftime("%y/%m/%d %H:%M:%S", time.localtime(item['created']/1000)) + ";" + str(args.league_id) + ";drop;" + str(item['type']) + ";" + str(item['status']) + ";" + team_name.encode('utf-8').strip() + ";" + drops_player_name.encode('utf-8').strip() + ";" + drops_positions[:-1] + ";" + str(bid) + "\n")
        
        if args.debug == "true":
            print("Saving file: " + transactions_filename)
        file_object.close()
    except Exception as e:
        raise


filename_prefix = "./data/transactions_rosters_" + args.league_id + "_" + args.week

# Players
players_file_path = "./data/players.json"
players_file_exists = exists(players_file_path)
if players_file_exists:
    if args.debug == "true":
        print("Skipping players")
else:
    if args.debug == "true":
        print("Getting players")
    players_file = open(players_file_path, "w")
    players_contents = urllib2.urlopen("https://api.sleeper.app/v1/players/nfl").read()
    players_file.write(str(players_contents))
    players_file.close()

# Rosters
rosters_file_path = filename_prefix + "_rosters.json"
rosters_file_exists = exists(rosters_file_path)
if rosters_file_exists:
    if args.debug == "true":
        print("Skipping rosters")
else:
    if args.debug == "true":
        print("Getting rosters")
    rosters_file = open(rosters_file_path, "w")
    rosters_contents = urllib2.urlopen("https://api.sleeper.app/v1/league/" + args.league_id + "/rosters").read()
    rosters_file.write(str(rosters_contents))
    rosters_file.close()

# Users
users_file_path = filename_prefix + "_users.json"
users_file_exists = exists(users_file_path)
if users_file_exists:
    if args.debug == "true":
        print("Skipping users")
else:
    if args.debug == "true":
        print("Getting users")
    users_file = open(users_file_path, "w")
    users_contents = urllib2.urlopen("https://api.sleeper.app/v1/league/" + args.league_id + "/users").read()
    users_file.write(str(users_contents))
    users_file.close()

# Transactions
transactions_file_path = filename_prefix + "_transactions.json"
transactions_file_exists = exists(transactions_file_path)
if transactions_file_exists:
    if args.debug == "true":
        print("Skipping transactions")
else:
    if args.debug == "true":
        print("Getting transactions")
    transactions_file = open(transactions_file_path, "w")
    transactions_contents = urllib2.urlopen("https://api.sleeper.app/v1/league/" + args.league_id + "/transactions/" + args.week).read()
    transactions_file.write(str(transactions_contents))
    transactions_file.close()

try:
    with open(transactions_file_path) as transactions_file:
        data = json.load(transactions_file)
        with open(players_file_path) as players_file:
            players = json.load(players_file)
            with open(rosters_file_path) as rosters_file:
                rosters = json.load(rosters_file)
                with open(users_file_path) as users_file:
                    users = json.load(users_file)
                    print_transactions(data, rosters, users, players)
except Exception as e:
    print(str(e))
