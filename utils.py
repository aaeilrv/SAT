from datetime import datetime, timedelta
from itertools import combinations
import subprocess
from icalendar import Calendar, Event

def o_clock(date_time, moment):
    if date_time.minute != 0 or date_time.second != 0 or date_time.microsecond != 0:
        if moment == "start":
            date_time += timedelta(hours=1)
        elif moment == "end":
            date_time -= timedelta(hours=1)
        date_time = date_time.replace(minute=0, second=0, microsecond=0)
    return date_time

def get_posible_games(n_players, n_days, n_hours):
    x = []
    for j1 in range(n_players):
        for j2 in range(n_players):
            for d in range(n_days):
                for h in range(n_hours):
                    if j1 != j2:
                        x.append((j1, j2, d, h))
    return x

def no_x_or_no_y(curr_possible_games, possible_games, rest):
    subsets = combinations(curr_possible_games, 2)
    for set in subsets:
        x = possible_games.index(set[0])+1
        y = possible_games.index(set[1])+1

        rest.append(f"-{x} -{y} 0\n")

# fix
def x_or_y(curr_possible_games, possible_games, rest):
    subsets = combinations(curr_possible_games, 2)
    for set in subsets:
        x = possible_games.index(set[0])+1
        y = possible_games.index(set[1])+1

        rest.append(f"{x} {y} 0\n")

def create_dimacs_file(x, rest_1, rest_2, rest_3, rest_4):
    # create the dimacs file
    f = open("tournament.dimacs", "w")
    f.write(f"p cnf {len(x)} {len(rest_1)+len(rest_3)+len(rest_4)}\n")
    for rest in rest_1:
        f.write(f"{rest}")
    #for rest in rest_2:
    #    f.write(f"{rest}")
    for rest in rest_3:
        f.write(f"{rest}")
    for rest in rest_4:
        f.write(f"{rest}")
    f.close()

def write_ical_file(all_games, solution, tournament_name, players_names, day, hour):
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//example.com//')
    cal.add('version', '2.0')
    cal.add('name', tournament_name)

    #event = Event()
    #event.add('tournament_name', tournament_name)

    solution = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 0"

    for sol in solution.split():
        if int(sol) > 0:
            encounter = all_games.get(int(sol))

            j1 = players_names.get(encounter[0]+1)
            j2 = players_names.get(encounter[1]+1)
            d = day.get(encounter[2]+1).strftime("%Y-%m-%d")
            h = hour.get(encounter[3]+1).strftime("%H:%M:%S")
            h2 = (hour.get(encounter[3]+1) + timedelta(hours=2)).strftime("%H:%M:%S")

            '''
            print(encounter)
            print("j1: ", j1)
            print("j2: ", j2)
            print("d: ", d)
            print("h: ", h)
            print("\n")
            '''

            event = Event()
            event.add('summary', f"{j1} vs {j2}")
            event.add('dtstart', datetime.strptime(f"{d} {h}", '%Y-%m-%d %H:%M:%S'))
            event.add('dtend', datetime.strptime(f"{d} {h2}", '%Y-%m-%d %H:%M:%S'))
            cal.add_component(event)

    # write .ics file
    f = open(f"{tournament_name}.ics", "wb")
    f.write(cal.to_ical())
    f.close()


def create_ical(games, tournament_name, players_names, days, hours):
    # call glucose
    subprocess.call(["./glucose-4.2.1/simp/glucose", "tournament.dimacs", "glucose-solution.txt", "-model", "-verb=0"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # check if solution exists
    with open("glucose-solution.txt", 'r') as file:
        solution = file.readline().strip()
        file.close()
    if solution == "UNSAT":
        print("Solution not found")
    else:
        write_ical_file(games, solution, tournament_name, players_names, days, hours)