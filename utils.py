from datetime import timedelta
from itertools import combinations
import subprocess
#import icalendar

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

def write_ical_file(games, solution):
    print("Solution found")	
    #cal = Calendar()
    #cal.add('prodid', '-//My calendar product//example.com//')
    #cal.add('version', '2.0')


def create_ical(games):
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
        write_ical_file(games, solution)