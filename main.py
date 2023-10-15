import argparse
import game.breakthrough as breakthrough
import agents.mm_agent as mm_agent
import agents.mcts_agent as mcts_agent
import misc.play as play
from timeit import default_timer as timer

# Set up and parse command-line arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--board", default=6, help="Board size (nxn).", type=int)
ap.add_argument("-g", "--games", default=1, help="Number of games to play (with each color).", type=int)
ap.add_argument("-a", "--abort", default='iterations', choices=['iterations', 'nodes', 'time_ms'],
                help="Type of search control to use, time, number of nodes, or iterations (iteration depth for mm,\
                      number of simulation for MCTS)", type=str)
ap.add_argument("-n", "--number", default=2, help="Value to abort on (depth, nodes, or msec)", type=int)
ap.add_argument("-e", "--eval", default=0, help="Use evaluation function number n (0 or 1)", type=int)
ap.add_argument("-d", "--verbose", default=0, help="Increase output verbosity.", type=int)
args = vars(ap.parse_args())
print(args)

# Set configuration variables to argument values.
board_size = args['board']
num_games = args['games']
agent_params = {'abort': args['abort'], 'number': args['number'], 'eval': args['eval'], 'verbose': args['verbose']}

# Set up the game and agents.
game = breakthrough.Breakthrough(board_size, board_size)
# agents = [ab_agent.ABAgent('1', agent_params),
#          mm_agent.MMAgent('1', agent_params),
#          random_agent.RandomAgent('1', agent_params),
#          greedy_agent.GreedyAgent('1', agent_params)]

agents = [mm_agent.MMAgent('1', agent_params),
          mcts_agent.MCTSAgent('1', agent_params)]

# Run a tournament and show the results.
start_time = timer()
game_records = play.play_a_tournament(game, agents, num_games, True if args['verbose'] > 0 else False)
print('Tournament results (', round(timer() - start_time, 2), 'sec. )')
score_color, score_agents = play.score_game_records(game_records, agents)
print(score_color, score_agents)


# NOTE: iterations vs. depth.