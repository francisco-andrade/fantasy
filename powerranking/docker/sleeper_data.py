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
parser.add_argument("--report", help="report", default="power")
parser.add_argument("--league_id", help="league_id", default="1")
parser.add_argument("--week", help="week", default="1")
parser.add_argument("--debug", help="debug", default="false")
args = parser.parse_args()

def print_power(rosters, week):
    for roster in rosters:
        team_recent_avg_points = 0
        counting_weeks = 1
        week_values = ""
        points_counter = 0
        bye_week=0
        if int(week) == 1:
            matchups_file_path = get_matchups(1)
            with open(matchups_file_path) as matchups_file:
                matchups = json.load(matchups_file)
            for matchup in matchups:
                if matchup['roster_id'] == roster['roster_id']:
                    points_counter = int(points_counter) + int(matchup['points'])
                    week_values = str(matchup['points']) + ";"
        if int(week) == 2:
            counting_weeks = 2
            for current_week in range(1,3):
                matchups_file_path = get_matchups(current_week)
                with open(matchups_file_path) as matchups_file:
                    matchups = json.load(matchups_file)
                for matchup in matchups:
                    if matchup['roster_id'] == roster['roster_id']:
                        points_counter = int(points_counter) + int(matchup['points'])
                        week_values = week_values + str(matchup['points']) + ";"
        if int(week) >= 3:
            counting_weeks = 3
            for current_week in range(int(week)-2,int(week)+1):
                matchups_file_path = get_matchups(current_week)
                with open(matchups_file_path) as matchups_file:
                    matchups = json.load(matchups_file)
                    for matchup in matchups:
                        if matchup['roster_id'] == roster['roster_id']:
                            if matchup['custom_points'] == 0:
                                bye_week=1
                            else: 
                                points_counter = float(points_counter) + float(matchup['points'])
                                week_values = week_values + str(matchup['points']) + ";"
        weeks_total = counting_weeks - bye_week
        team_recent_avg_points = points_counter / weeks_total
        team_record = str("%02d" % ((roster['settings']['wins']/(roster['settings']['wins']+roster['settings']['losses'])*100),))
        print(str(week) + ";" + str(args.league_id) + "_" + str(roster['owner_id']) + ";" + str(args.league_id) + ";" + str(roster['owner_id']) + ";" + str(roster['roster_id']) + ";" + str(roster['settings']['wins'],) + ";" + str(roster['settings']['losses']) + ";" + str(roster['settings']['ties']) + ";" + str(roster['settings']['fpts']) + ";" + str(team_record) + ";" + str("%.2f" % team_recent_avg_points) + ";" + week_values[:-1])

def print_users(users):
    for user in users:
        try:
            print(str(args.league_id) + "_" + str(user['user_id']) + ";" + str(user['league_id']) + ";"  + str(user['user_id']) + ";" + str(user['display_name']) + ";" + str(user['metadata']['team_name']) )
        except:
            print(str(args.league_id) + "_" + str(user['user_id']) + ";" + str(user['league_id']) + ";"  + str(user['user_id']) + ";" + str(user['display_name']) + ";NA")

def get_rosters():
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
    return rosters_file_path

def get_matchups(week_number):
    matchups_file_path = filename_prefix + "_" + str(week_number) + "_" + "matchups.json"
    matchups_file_exists = exists(matchups_file_path)
    if matchups_file_exists:
        if args.debug == "true":
            print("Skipping matchups")
    else:
        if args.debug == "true":
            print("Getting matchups")
        matchups_file = open(matchups_file_path, "w")
        matchups_contents = urllib2.urlopen("https://api.sleeper.app/v1/league/" + args.league_id + "/matchups/" + str(week_number)).read()
        matchups_file.write(str(matchups_contents))
        matchups_file.close()
    return matchups_file_path

def get_users():
    users_file_path = filename_prefix + "_" + "users.json"
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
    return users_file_path

if args.report == "power":
    filename_prefix = "./data/" +  args.league_id + "_power_"
    try:
        rosters_file_path = get_rosters()
        with open(rosters_file_path) as rosters_file:
            rosters = json.load(rosters_file)
            print_power(rosters, args.week)
    except Exception as e:
        print(str(e))

if args.report == "users":
    filename_prefix = "./data/" +  args.league_id + "_users_"
    try:
        users_file_path = get_users()
        with open(users_file_path) as users_file:
            users = json.load(users_file)
            print_users(users)
    except Exception as e:
        print(str(e))
