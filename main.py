from datetime import datetime, timedelta
from utils import o_clock, get_posible_games, create_dimacs_file, create_ical
from restrictions import get_rest_1, get_rest_2, get_rest_3, get_rest_4
import json
import sys

if __name__ == '__main__':
    # open json file and transform into a dictionary
    with open(sys.argv[1]) as json_file:
        data = json.load(json_file)

    json_file.close()

    # save data into variables
    game_length = 2 # each game lasts 2 hours
    tournament_name = data['tournament_name']
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    start_time = datetime.strptime(data['start_time'], '%H:%M:%S.%f')
    end_time = datetime.strptime(data['end_time'], '%H:%M:%S.%f')
    players_names = data['participants']
    num_players = len(data['participants'])

    start_time = o_clock(start_time, "start")
    end_time = o_clock(end_time, "end")

    # calculate the total time of the game
    days = end_date - start_date
    
    hours = end_time - start_time
    n_hours = hours.seconds//3600 + 1

    n_days = days.days + 1
    total_slots_per_day = n_hours // game_length
    
    x = get_posible_games(num_players, n_days, total_slots_per_day)

    rest_1 = get_rest_1(num_players, n_days, total_slots_per_day, x)
    print("rest 1 encoded")

    rest_2 = get_rest_2(num_players, n_days, total_slots_per_day, x)
    print("rest 2 encoded")

    rest_3 = get_rest_3(num_players, n_days, total_slots_per_day, x)
    print("rest 3 encoded")

    rest_4 = get_rest_4(num_players, n_days, total_slots_per_day, x)
    print("rest_4 encoded")

    create_dimacs_file(x, rest_1, rest_2, rest_3, rest_4)
    print(".dimacs file created")
    
    # mappings
    games_mapping = {}
    for i in range(len(x)):
        games_mapping[i+1] = x[i]

    players_mapping = {}
    for i in range(len(players_names)):
        players_mapping[i+1] = players_names[i]

    days_mapping = {}
    for i in range(n_days):
        days_mapping[i+1] = start_date + timedelta(days=i)

    hours_mapping = {}
    for i in range(total_slots_per_day):
        hours_mapping[i+1] = start_time + timedelta(hours=i*2)

    # create iCalendar file
    create_ical(games_mapping, tournament_name, players_mapping, days_mapping, hours_mapping)