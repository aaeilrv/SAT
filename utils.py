from datetime import timedelta
from itertools import combinations

def o_clock(date_time):
    if date_time.minute != 0 or date_time.second != 0:
        date_time += timedelta(hours=1)
        date_time = date_time.replace(minute=0, second=0)
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

# 1. Dos juegos no pueden ocurrir al mismo tiempo.
# CNF:(not a or not b)
# (X(j1, j2, d, h) or X(j3, j4, d, h)) and (not X(j1, j2, d, h) or not X(j3, j4, d, h))
def get_rest_1(n_players, n_days, n_hours, possible_games):
    rest = []

    for d in range(n_days):
        for h in range(n_hours):
            curr_possible_games = []
            for j1 in range(n_players):
                for j2 in range(n_players):
                    if j1 != j2:
                        curr_possible_games.append((j1, j2, d, h))

            subsets = combinations(curr_possible_games, 2)
            for set in subsets:
                x = possible_games.index(set[0])+1
                y = possible_games.index(set[1])+1

                rest.append(f"-{x} -{y} 0")
    return rest

# 2. Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una
# como "visitante" y la otra como "local".
# CNF: (not a or b) and (b or not a)
# not X(j1, j2, d1, h1) or X(j2, j1, d2, h2)
def get_rest_2(n_players, n_days, n_hours):
    rest_2 = []
    for j1 in range(n_players):
        for j2 in range(n_players):
            for d1 in range(n_days):
                for d2 in range(n_days):
                    for h1 in range(n_hours):
                        for h2 in range(n_hours):
                            if j1 != j2 and d1 != d2:
                                rest_2.append([(j1, j2, d1, h1), (j2, j1, d2, h2)])
                                rest_2.append([(j2, j1, d1, h1), (j1, j2, d2, h2)])
    return rest_2

# 3. Un jugador solo puede jugar maximo una vez por dia
# CNF: not a or not b or not c
# not X(j1, j2, d, h1) or not X(j1, j3, d, h2) or not X(j3, j1, d, h2)
def get_rest_3(n_players, n_days, n_hours):
    rest_3 = []
    for j1 in range(n_players):
        for j2 in range(n_players):
            for j3 in range(n_players):
                for d in range(n_days):
                    for h1 in range(n_hours):
                        for h2 in range(n_hours):
                            if j1!=j2 and j1 != j3 and h1!=h2:
                                rest_3.append([(j1, j2, d, h1), 
                                               (j1, j3, d, h2), (j3, j1, d, h2)])
    return rest_3

# 4. Un participante no puede jugar de "visitante" en dos días consecutivos,
# ni de "local" dos días seguidos.
# CNF: not a or not b
# not X(j1, j2, d1, h1) or not X(j1, j2, d2, h2)
def get_rest_4(n_players, n_days, n_hours):
    rest_4 = []
    for j1 in range(n_players):
        for j2 in range(n_players):
            for j3 in range(n_players):
                for d in range(n_days-1):
                    for h1 in range(n_hours):
                        for h2 in range(n_hours):
                            if j1 != j2 and j1 != j3:
                                rest_4.append([(j1, j2, d, h1), (j1, j3, d+1, h2)])
                                rest_4.append([(j2, j1, d, h1), (j3, j1, d+1, h2)])

    return rest_4

def create_dimacs_file(x, rest_1, rest_2, rest_3, rest_4):
    # create the dimacs file
    f = open("tournament.dimacs", "w")
    f.write(f"p cnf {len(x)} {len(rest_1)} \n")
    for rest in rest_1:
        f.write(f"{rest} \n")
    f.close()