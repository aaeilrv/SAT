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