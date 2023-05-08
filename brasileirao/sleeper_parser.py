#!/usr/bin/python
# python ./sleeper_converter.py --option players --file file.json --output csv
from __future__ import division
import sys
import json
import argparse
import urllib2
import time
from os.path import exists

parser = argparse.ArgumentParser()
parser.add_argument("--option", help="options: draft, players, player", default="player")
parser.add_argument("--output", help="outputs: csv", default="csv")
parser.add_argument("--league_id", help="league_id", default="0")
parser.add_argument("--week", help="week", default="1")
args = parser.parse_args()

league_id = args.league_id
week_number = args.week

def check_value(data, key, default):
    try:
        if key in data:
            return str(data[key])
        else:
            return default
    except Exception:
        return default

def print_rosters(data, output):
    for item in data:
        owner = item['owner_id']
        for starter in item['starters']:
            print(owner + ";" + str(item['settings']['wins']) + ";" + starter + ";STARTER")
        for reserve in item['reserve']:
            print(owner  + ";" + str(item['settings']['wins']) + ";" + reserve + ";BENCH")

def print_roster_ids(data, output):
    for item in data:
        print(str(league_id) + "_" + str(item['roster_id']) + ";" + str(league_id) + ";" + str(item['roster_id']) + ";" + str(item['owner_id']))

def print_users(data, output):
    for item in data:
        try:
            print(str(league_id) + "_" + str(item['user_id']) + ";" + str(item['league_id']) + ";"  + str(item['user_id']) + ";" + str(item['display_name']) + ";" + str(item['metadata']['team_name']) )
        except:
            print(str(league_id) + "_" + str(item['user_id']) + ";" + str(item['league_id']) + ";"  + str(item['user_id']) + ";" + str(item['display_name']) + ";NA")

def print_matchups(data, output):
    try:
        with open(rosters_file_path) as rosters_file:
            rosters = json.load(rosters_file)
            for item in data:
                for roster in rosters:
                    if roster['roster_id'] == item['roster_id']:
                        wins = str(roster['settings']['wins'])
                        loses = str(roster['settings']['losses'])
                        ties = str(roster['settings']['ties'])
                        points = str(roster['settings']['fpts'])
                        owner = str(roster['owner_id'])
                print(str(week_number) + ";" + str(league_id) + ";" + str(item['roster_id']) + ";" + owner  + ";" + str(item['matchup_id']) + ";" + str(item['points']) + ";" + wins + ";" + loses + ";" + ties + ";" + points)
    except Exception as e:
        print(str(e))

def print_teams_data(data, output):
    for item in data:
        record = str(item['metadata']['record'])
        print(item['owner_id'] + ";" + str(item['settings']['wins']) + ";" + str(item['settings']['wins']) + ";" + str(item['settings']['losses']) + ";" + str(item['settings']['fpts']) + ";" + str(item['settings']['waiver_position']) + ";" + record)

def print_leagues(data, output):
    for item in data:
        print(str(item['league_id']) + ";" + item['name'].encode('utf-8').strip())


filename_prefix = "./data/matchups_" + league_id + "_" + week_number

# Players
players_file_path = "./data/players.json"
def get_players():
    players_file_exists = exists(players_file_path)
    if not players_file_exists:
        players_file = open(players_file_path, "w")
        players_contents = urllib2.urlopen("https://api.sleeper.app/v1/players/nfl").read()
        players_file.write(str(players_contents))
        players_file.close()

# Rosters
def get_rosters(p_league_id):
    rosters_file_exists = exists(rosters_file_path)
    if not rosters_file_exists:
        rosters_file = open(rosters_file_path, "w")
        rosters_contents = urllib2.urlopen("https://api.sleeper.app/v1/league/" + p_league_id + "/rosters").read()
        rosters_file.write(str(rosters_contents))
        rosters_file.close()


# Users
def get_users(p_league_id):
    users_file_exists = exists(users_file_path)
    if not users_file_exists:
        users_file = open(users_file_path, "w")
        users_contents = urllib2.urlopen("https://api.sleeper.app/v1/league/" + p_league_id + "/users").read()
        users_file.write(str(users_contents))
        users_file.close()

# Matchups
def get_matchups(p_league_id, p_week_number):
    matchups_file_exists = exists(matchups_file_path)
    if not matchups_file_exists:
        matchups_file = open(matchups_file_path, "w")
        matchups_contents = urllib2.urlopen("https://api.sleeper.app/v1/league/" + p_league_id + "/matchups/" + p_week_number).read()
        matchups_file.write(str(matchups_contents))
        matchups_file.close()


leagues_file = "./data/leagues_2022.txt"
try:
    with open(leagues_file) as league_file:
        mylist = league_file.read().splitlines()
        for row in mylist:
            rosters_file_path = filename_prefix + "_rosters.json"
            users_file_path = filename_prefix + "_users.json"
            matchups_file_path = filename_prefix + "_matchups.json"
            get_rosters(row)
            get_users(row)
            get_matchups(row, week_number)
            league_id = row
            if args.option == "roster-ids":
                with open(rosters_file_path) as json_file:
                    data = json.load(json_file)
                    print_roster_ids(data, args.output)
            if args.option == "users":
                with open(users_file_path) as json_file:
                    data = json.load(json_file)
                    print_users(data, args.output)
            if args.option == "matchups":
                with open(matchups_file_path) as json_file:
                    data = json.load(json_file)
                    print_matchups(data, args.output)
except Exception as e:
    print(str(e))
