from datetime import datetime
from utils import o_clock
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
    n_days = days.days
    
    hours = end_time - start_time
    n_hours = hours.seconds//3600

    total_days = days.days + 1 # add 1 because the last day is included
    total_slots_per_day = hours / game_length
    total_slots = total_days * total_slots_per_day

    # pasar info pa que se resuelva la cosa

    # x(j1, j2, d, h) = el jugados j1 (local) juega contra j2 (visitante) el dia d a la hora h
    # buscamos todos los posibles juegos (asi se vayan a jugar o no)
    x = []
    for j1 in range(num_players):
        for j2 in range(num_players):
            for d in range(n_days):
                for h in range(n_hours):
                    x.append((j1, j2, d, h))

    # primera restriccion
    # dos juegos no pueden ocurrir al mismo tiempo
    # (all j1, j2, j3, j4, d, h | j1 != j2 and j3 != j4 and X(j1,j2,d,h): not X(j3, j4, d, h))
    
    # transformado queda
    # (all j1, j2, j3, j4, d, h|: not X(j1, j2, d, h) or not(j3, j4, d, h))
    rest_1 = [] # (not x_i, not x_j)
    for j1 in range(num_players):
        for j2 in range(num_players):
            for j3 in range(num_players):
                for j4 in range(num_players):
                    for d in range(n_days):
                        for h in range(n_hours):
                            if (j1 != j2 and j3 != j4):
                                rest_1.append([(j1, j2, d, h), (j3, j4, d, h)])

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

    # tercera reestriccion
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
        values_mapping[i[0]] = index

        index = x.index(i[1])
        values_mapping[i[1]] = index
