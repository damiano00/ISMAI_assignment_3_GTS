import agents.agent as agent
import random


class GreedyAgent(agent.Agent):

    def __init__(self, name, params):
        # random.seed(42)
        super().__init__(params, f'greedy_agent_{name}')

    def play(self, game):
        # Plays a random winning moves if one exists, otherwise a capture move, otherwise any move.
        winning_moves = []
        capture_moves = []
        moves = game.generate()
        for m in moves:
            game.make(m)
            if game.is_terminal():
                winning_moves.append(m)
            game.retract(m)
            if m[2] != game.get_board().NoPce:
                capture_moves.append(m)
        return random.choice(winning_moves) if winning_moves \
                      else random.choice(capture_moves) if capture_moves else random.choice(moves)
