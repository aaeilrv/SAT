from datetime import timedelta

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

def get_rest_1(n_players, n_days, n_hours):
    # not xi or not xj
    rest_1 = []

    for j1 in range(n_players):
        for j2 in range(n_players):
            for j3 in range(n_players):
                for j4 in range(n_players):
                    for d in range(n_days):
                        for h in range(n_hours):
                            if (j1 != j2 and j3 != j4):
                                rest_1.append([(j1, j2, d, h), (j3, j4, d, h)])

    return rest_1

def get_rest_2(n_players, n_days, n_hours):
    # segunda restriccion
    # Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una
    # como "visitante" y la otra como "local".
    # (all j1, j2, d, h |: not X(j1, j2, d, h) or X(j2, j1, d, h))

    rest_2 = []

    for j1 in range(n_players):
        for j2 in range(n_players):
            for d in range(n_days):
                for h in range(n_hours):
                    if (j1 != j2):
                        rest_2.append([(j1, j2, d, h), (j2, j1, d, h)])

    return rest_2

def get_rest_3(n_players, n_days, n_hours):
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
    for j1 in range(n_players):
        for j2 in range(n_players):
            for j3 in range(n_players):
                for d in range(n_days):
                    for h1 in range(n_hours):
                        for h2 in range(n_hours):
                            if j1!=j2 and j3!=j1 and j3!=j2 and h1!=h2:
                                rest_3.append([(j1, j2, d, h1), 
                                               (j1, j3, d, h2), (j3, j1, d, h2), 
                                               (j2, j3, d, h2), (j3, j2, d, h2), 
                                               (j1, j2, d, h2), (j2, j1, d, h2)])
    return rest_3

def get_rest_4(n_players, n_days, n_hours):
    # cuarta restriccion
    # Un participante no puede jugar de "visitante" en dos días consecutivos,
    # ni de "local" dos días seguidos.
    # (all j1, j2, d, h | j1 != j2 and X(j1, j2, d, h) : not X(j1, j2, d+1, h))
    # (all j1, j2, d, h | j1 != j2 and X(j2, j1, d, h) : not X(j2, j1, d+1, h))

    # transformando queda
    # (all j1, j2, d, h |: not X(j1, j2, d, h) or not X(j1, j2, d+1, h))
    # (all j1, j2, d, h |: not X(j2, j1, d, h) or not X(j2, j1, d+1, h))

    rest_4 = []
    for j1 in range(n_players):
        for j2 in range(n_players):
            for d in range(n_days-1):
                for h in range(n_hours):
                    if j1 != j2:
                        rest_4.append([(j1, j2, d, h), (j1, j2, d+1, h)])
                        rest_4.append([(j2, j1, d, h), (j2, j1, d+1, h)])

    return rest_4

def create_dimacs_file(x, rest_1, rest_2, rest_3, rest_4):
    # create the dimacs file
    clausules = []
    for clausule in rest_1:
        i = x.index(clausule[0])
        j = x.index(clausule[1])

        clausules.append(f"-{i+1} -{j+1} 0")

    for clausule in rest_2:
        i = x.index(clausule[0])
        j = x.index(clausule[1])

        clausules.append(f"-{i+1} {j+1} 0")
    
    for clausule in rest_4:
        i = x.index(clausule[0])
        j = x.index(clausule[1])

        clausules.append(f"-{i+1} -{j+1} 0")
    

    f = open("tournament.dimacs", "w")
    f.write(f"p cnf {len(x)} {len(clausules)} \n")
    for clausule in clausules:
        f.write(f"{clausule} \n")
    f.close()