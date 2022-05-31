#!/usr/bin/python
# python ./sleeper_converter.py --option players --file file.json --output csv
from __future__ import division
import sys
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="file path")
parser.add_argument("--rosters", help="rosters file path")
parser.add_argument("--option", help="options: draft, players, player", default="player")
parser.add_argument("--player_id", help="player_id", default="null")
parser.add_argument("--output", help="outputs: csv", default="csv")
parser.add_argument("--league_id", help="league_id", default="0")
parser.add_argument("--league_name", help="league_id", default="NA")
parser.add_argument("--week", help="week", default="1")
args = parser.parse_args()

def print_player(data, player_id, output):
    print(json.dumps(data[player_id]))

def check_value(data, key, default):
    try:
        if key in data:
            return str(data[key])
        else:
            return default
    except Exception:
        return default

def print_players(data, output):
    for item in data:
        player_data = data[item]
        try:
            #position = str(player_data['position'])
            position = str(player_data['fantasy_positions'])
            player_id = str(player_data['player_id'])
            full_name = str(player_data['first_name']) + " " + str(player_data['last_name'])
            team = check_value(player_data, 'team', 'None')
            search_rank = check_value(player_data, 'search_rank', '9999999')
            years_exp = check_value(player_data, 'years_exp', 'None')
            age = check_value(player_data, 'age', 'None')
            college = check_value(player_data, 'college', 'None')
            years_exp = check_value(player_data, 'years_exp', 'None')
            print(player_id + ";" + full_name + ";" + position + ";" + team + ";" + search_rank + ";" + age + ";" + college + ";" + years_exp)
        except:
            print("error;player;" + player_id + "-;-;-")

def print_draft(data, output):
    if args.output == "json":
        print(json.dumps(data))
    else:
        for item in data:
            try:
                print( str(args.league_name) + ";" + str(item['player_id']) + ";" + str(item['metadata']['first_name']) + " " + str(item['metadata']['last_name']) + ";" + str(item['round']) + ";" + str(item['pick_no']) + ";" + str(item['picked_by']) + ";" + str(item['metadata']['position']) + ";" + str(item['metadata']['team']))
            except:
                print("error;" + str(item))

def print_rosters(data, output):
    for item in data:
        owner = item['owner_id']
        for starter in item['starters']:
            print(owner + ";" + str(item['settings']['wins']) + ";" + starter + ";STARTER")
        for reserve in item['reserve']:
            print(owner  + ";" + str(item['settings']['wins']) + ";" + reserve + ";BENCH")

def print_roster_ids(data, output):
    for item in data:
        print(str(args.league_id) + "_" + str(item['roster_id']) + ";" + str(args.league_id) + ";" + str(item['roster_id']) + ";" + str(item['owner_id']))

def print_users(data, output):
    for item in data:
        try:
            print(str(args.league_id) + "_" + str(item['user_id']) + ";" + str(item['league_id']) + ";"  + str(item['user_id']) + ";" + str(item['display_name']) + ";" + str(item['metadata']['team_name']) )
        except:
            print(str(args.league_id) + "_" + str(item['user_id']) + ";" + str(item['league_id']) + ";"  + str(item['user_id']) + ";" + str(item['display_name']) + ";NA")

def print_matchups(data, output):
    try:
        with open(args.rosters) as rosters_file:
            rosters = json.load(rosters_file)
            for item in data:
                for roster in rosters:
                    if roster['roster_id'] == item['roster_id']:
                        wins = str(roster['settings']['wins'])
                        loses = str(roster['settings']['losses'])
                        ties = str(roster['settings']['ties'])
                        points = str(roster['settings']['fpts'])
                        owner = str(roster['owner_id'])
                print(str(args.week) + ";" + str(args.league_id) + ";" + str(item['roster_id']) + ";" + owner  + ";" + str(item['matchup_id']) + ";" + str(item['points']) + ";" + wins + ";" + loses + ";" + ties + ";" + points)
    except Exception as e:
        print(str(e))

def print_teams_data(data, output):
    for item in data:
        record = str(item['metadata']['record'])
        print(item['owner_id'] + ";" + str(item['settings']['wins']) + ";" + str(item['settings']['wins']) + ";" + str(item['settings']['losses']) + ";" + str(item['settings']['fpts']) + ";" + str(item['settings']['waiver_position']) + ";" + record)

def print_leagues(data, output):
    for item in data:
        print(str(item['league_id']) + ";" + item['name'].encode('utf-8').strip())

def print_power(data, output):
    for item in data:
        team_record = str("%02d" % ((item['settings']['wins']/(item['settings']['wins']+item['settings']['losses'])*100),))
        print(str(args.week) + ";" + str(args.league_id) + "_" + str(item['owner_id']) + ";" + str(args.league_id) + ";" + str(item['owner_id']) + ";" + str(item['roster_id']) + ";" + str(item['settings']['wins'],) + "-" + str(item['settings']['losses']) + "-" + str(item['settings']['ties']) + ";" + str(item['settings']['fpts']) + ";" + team_record)


try:
    with open(args.file) as json_file:
        data = json.load(json_file)
        if args.option == "draft":
            print_draft(data, args.output)
        elif args.option == "players":
            print_players(data, args.output)
        elif args.option == "player":
            print_player(data, args.player_id, args.output)
        elif args.option == "rosters":
            print_rosters(data, args.output)
        elif args.option == "teams":
            print_teams_data(data, args.output)
        elif args.option == "matchups":
            print_matchups(data, args.output)
        elif args.option == "roster-ids":
            print_roster_ids(data, args.output)
        elif args.option == "users":
            print_users(data, args.output)
        elif args.option == "leagues":
            print_leagues(data, args.output)
        elif args.option == "power":
            print_power(data, args.output)
except Exception as e:
    print(str(e))
