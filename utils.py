from datetime import timedelta
from itertools import combinations

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

# 1. Dos juegos no pueden ocurrir al mismo tiempo.
def get_rest_1(n_players, n_days, n_hours, possible_games):
    rest = []
    for d in range(n_days):
        for h in range(n_hours):
            curr_possible_games = []
            for j1 in range(n_players):
                for j2 in range(n_players):
                    if j1 != j2:
                        curr_possible_games.append((j1, j2, d, h))

            no_x_or_no_y(curr_possible_games, possible_games, rest)

    return rest

# 2. Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una
# como "visitante" y la otra como "local".
def get_rest_2(n_players, n_days, n_hours, possible_games):
    rest = []
    for j1 in range(n_players):
            for j2 in range(n_players):
                curr_possible_games = []
                for d in range(n_days):
                    for h in range(n_hours):
                        if j1 != j2:
                            curr_possible_games.append((j1, j2, d, h))

                no_x_or_no_y(curr_possible_games, possible_games, rest)
                x_or_y(curr_possible_games, possible_games, rest)

    return rest

# 3. Un jugador solo puede jugar maximo una vez por dia
def get_rest_3(n_players, n_days, n_hours, possible_games):
    rest = []

    for j1 in range(n_players):
        for d in range(n_days):
            curr_posible_games = []
            for j2 in range(n_players):
                for h in range(n_hours):
                    if j1 != j2:
                        curr_posible_games.append((j1, j2, d, h))
                        curr_posible_games.append((j2, j1, d, h))

            no_x_or_no_y(curr_posible_games, possible_games, rest)  

    return rest

# 4. Un participante no puede jugar de "visitante" en dos días consecutivos,
# ni de "local" dos días seguidos.
def get_rest_4(n_players, n_days, n_hours, possible_games):
    rest = []
    # un equipo no puede jugar local dos dias consecutivos seguidos
    for j1 in range(n_players):
        for d in range(n_days-1):
            curr_posible_games = []
            for j2 in range(n_players):
                for h in range(n_hours):
                    if j1 != j2:
                        curr_posible_games.append((j1, j2, d, h))
                        curr_posible_games.append((j1, j2, d+1, h))

            no_x_or_no_y(curr_posible_games, possible_games, rest)


    # un equipo no puede jugar dos dias consecutivos como visitante
    for j1 in range(n_players):
        for d in range(n_days-1):
            curr_posible_games = []
            for j2 in range(n_players):
                for h in range(n_hours):
                    if j1 != j2:
                        curr_posible_games.append((j2, j1, d, h))
                        curr_posible_games.append((j2, j1, d, h))

            no_x_or_no_y(curr_posible_games, possible_games, rest)
    
    return rest

def create_dimacs_file(x, rest_1, rest_2, rest_3, rest_4):
    # create the dimacs file
    f = open("tournament.dimacs", "w")
    f.write(f"p cnf {len(x)} {len(rest_1)+len(rest_2)+len(rest_3)+len(rest_4)}\n")
    for rest in rest_1:
        f.write(f"{rest}")
    for rest in rest_2:
        f.write(f"{rest}")
    for rest in rest_3:
        f.write(f"{rest}")
    for rest in rest_4:
        f.write(f"{rest}")
    f.close()