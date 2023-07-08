from datetime import datetime
from utils import o_clock, get_posible_games, get_rest_1
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

    start_time = o_clock(start_time)
    end_time = o_clock(end_time)

    # calculate the total time of the game
    days = end_date - start_date
    
    hours = end_time - start_time
    n_hours = hours.seconds//3600

    n_days = days.days + 1
    total_slots_per_day = hours / game_length
    total_slots = n_days * total_slots_per_day

    # pasar info pa que se resuelva la cosa

    x = get_posible_games(num_players, n_days, n_hours)

    rest_1 = get_rest_1(num_players, n_days, n_hours)

    
    # segunda restriccion
    # Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una
    # como "visitante" y la otra como "local".
    # (all j1, j2, d, h |: not X(j1, j2, d, h) or X(j2, j1, d, h))

    rest_2 = []
    for j1 in range(num_players):
        for j2 in range(num_players):
            for d in range(n_days):
                for h in range(n_hours):
                    if (j1 != j2):
                        rest_2.append([(j1, j2, d, h), (j2, j1, d, h)])

    # tercera restriccion
    # un jugador solo puede jugar maximo una vez por dia
    # (all j1, j2, j3, d, h1, h2| j1 != j2 and j1 != j3 and j2 != j3 and X(j1, j2, d, h1): 
    #                               not X(j1, j3, d, h2) or not X(j3, j1, d, h2) or not X(j2, j3, d, h2) or 
    #                               not X(j3, j2, d, h2) or not X(j1, j2, d, h2) or not X(j2, j1, d, h2))

    # transformando queda
    #(all j1, j2, j3, d, h1, h2|:not X(j1, j2, d, h1) or 
    #                               not X(j1, j3, d, h2) or not X(j3, j1, d, h2) or not X(j2, j3, d, h2) or 
    #                               not X(j3, j2, d, h2) or not X(j1, j2, d, h2) or not X(j2, j1, d, h2))
    rest_3 = []
    for j1 in range(num_players):
        for j2 in range(num_players):
            for j3 in range(num_players):
                for d in range(n_days):
                    for h1 in range(n_hours):
                        for h2 in range(n_hours):
                            if j1 != j2 and not j3 in [j1, j2] and h1 != h2:
                                rest_3.append([(j1, j2, d, h1), 
                                               (j1, j3, d, h2), (j3, j1, d, h2), 
                                               (j2, j3, d, h2), (j3, j2, d, h2), 
                                               (j1, j2, d, h2), (j2, j1, d, h2)])

    #print(len(rest_3))

    # cuarta restriccion
    # Un participante no puede jugar de "visitante" en dos días consecutivos,
    # ni de "local" dos días seguidos.
    # (all j1, j2, d, h | j1 != j2 and X(j1, j2, d, h) : not X(j1, j2, d+1, h))
    # (all j1, j2, d, h | j1 != j2 and X(j2, j1, d, h) : not X(j2, j1, d+1, h))

    # transformando queda
    # (all j1, j2, d, h |: not X(j1, j2, d, h) or not X(j1, j2, d+1, h))
    # (all j1, j2, d, h |: not X(j2, j1, d, h) or not X(j2, j1, d+1, h))

    rest_4 = []
    for j1 in range(num_players):
        for j2 in range(num_players):
            for d in range(n_days):
                for h in range(n_hours):
                    if j1 != j2:
                        rest_4.append([(j1, j2, d, h), (j1, j2, d+1, h)])
                        rest_4.append([(j2, j1, d, h), (j2, j1, d+1, h)])

    rest = rest_1 + rest_2 + rest_3 + rest_4
    values_mapping = {}

    for i in rest:
        index = x.index(i[0])
        values_mapping[index] = i[0]

        index = x.index(i[1])
        values_mapping[index] = i[1]