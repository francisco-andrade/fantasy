#!/usr/bin/python
import sys
import json

def print_player_json(json_data, player_id):
    print json.dumps(json_data[player_id])

def print_players_csv(json_data):
    for item in data:
        try:
            if 'search_rank' in data[item]:
                if data[item]['position'] == None:
                    print(data[item]['full_name'] + ";None;" + str(data[item]['search_rank']))
                elif data[item]['position'] == 'DEF':
                    if 'search_rank' in data[item]:
                        print(data[item]['last_name'] + ";DEF;" + str(data[item]['search_rank']))
                    else:
                        print(data[item]['last_name'] + ";DEF;unknown")
                else:
                    print(data[item]['full_name'] + ";" + data[item]['position'] + ";" + str(data[item]['search_rank']))
            else:
                print(data[item]['last_name'] + ";" + data[item]['position'] + ";" + "unknown")
        except:
            print("error;player;" + str(data[item]))

filename = sys.argv[1]

try:
    with open(filename) as json_file:
        data = json.load(json_file)
        command = sys.argv[2]
        if command == 'csv':
            print_players_csv(data)
        else:
            player_id = sys.argv[3]
            print_player_json(data, player_id)
except Exception as e:
    print(str(e))
