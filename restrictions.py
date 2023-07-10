from utils import no_x_or_no_y, x_or_y

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