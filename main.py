from datetime import datetime
import json
import sys

if __name__ == '__main__':
    # open json file and transform into a dictionary
    with open(sys.argv[1]) as json_file:
        data = json.load(json_file)

    json_file.close()

    # save data into variables
    game_length = 2 # each game lasts 2 hours
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    start_time = datetime.strptime(data['start_time'], '%H:%M:%S')
    end_time = datetime.strptime(data['end_time'], '%H:%M:%S')
    num_players = len(data['participants'])

    # calculate the total time of the game
    days = end_date - start_date
    hours = end_time - start_time

    total_days = days.days + 1 # add 1 because the last day is included
    total_slots_per_day = hours / game_length
    total_slots = total_days * total_slots_per_day

    # pasar info pa que se resuelva la cosa
