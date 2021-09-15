#!/usr/bin/python
# python ./sleeper_converter.py --option players --file file.json --output csv

import sys
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="file path")
parser.add_argument("--option", help="options: draft, players, player", default="player")
parser.add_argument("--player_id", help="player_id", default="null")
parser.add_argument("--output", help="outputs: csv", default="csv")
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
            position = str(player_data['position'])
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
                print( str(item['player_id']) + ";" + str(item['round']) + ";" + str(item['pick_no']) + ";" + str(item['picked_by']) + ";" + str(item['metadata']['position']) + ";" + str(item['metadata']['team']) + ";" + str(item['metadata']['first_name']) + " " + str(item['metadata']['last_name']) + ";" + str(item['metadata']['years_exp']))
            except:
                print("error;" + str(item))

try:
    with open(args.file) as json_file:
        data = json.load(json_file)
        if args.option == "draft":
            print_draft(data, args.output)
        elif args.option == "players":
            print_players(data, args.output)
        elif args.option == "player":
            print_player(data, args.player_id, args.output)
except Exception as e:
    print(str(e))
