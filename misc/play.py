import misc.utils as utils
import copy


def score_game_records(game_records, agents):
    score_color = {'White': 0, 'Black': 0}
    score_agent = dict()
    for a in agents:
        score_agent[a.name()] = 0
    for record in game_records:
        if record[1] == 1:
            score_color['White'] += 1
            score_agent[record[0][0]] += 1
        elif record[1] == -1:
            score_color['Black'] += 1
            score_agent[record[0][1]] += 1
        else:
            print('Invalid score:', record[1])
    return score_color, score_agent


def play_a_game(game, players, disp_state):
    return_values = []
    game.setup()
    players[0].reset()
    players[1].reset()
    n = 0
    while not game.is_terminal():
        if disp_state:
            print(game)
        players[n % 2].reset()
        move = players[n % 2].play(copy.deepcopy(game))
        # move, value, max_i, moves, policy, q = players[n % 2].play(copy.deepcopy(game), utils.CheckAbort(time))
        assert(move != utils.NoMove)
        # return_values.append((move, value, max_i, moves, policy, q))
        game.make(move)
        n += 1
    outcome = -1 if game.get_to_move() == game.White else 1
    return [players[0].name(), players[1].name()], outcome, return_values


def play_a_match(game, agents, num_games, disp_state):
    game_records = []
    for _ in range(num_games):
        game_record = play_a_game(game, agents, disp_state)
        game_records.append(game_record)
        game_record = play_a_game(game, agents[::-1], disp_state)
        game_records.append(game_record)
    return game_records


def play_a_tournament(game, agents, num_games, disp_state):
    tournament_game_records = []
    for i in range(len(agents)-1):
        for j in range(i+1, len(agents)):
            match_agents = [agents[i], agents[j]]
            match_game_records = play_a_match(game, match_agents, num_games, disp_state)
            tournament_game_records += match_game_records
            print(*score_game_records(match_game_records, match_agents))

    return tournament_game_records
