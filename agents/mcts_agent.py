import agents.agent as agent
import mcts_search as search
import misc.utils as utils

class MCTSAgent(agent.Agent):

    def __init__(self, name, params):
        super().__init__(params, f'mcts_agent_{name}')
        abort_type = self._params.get('abort')
        if abort_type == 'iterations':
            self._abort_checker = utils.Aborter(utils.AbortType.ITERATIONS, self._params.get('number'))
        elif abort_type == 'nodes':
            self._abort_checker = utils.Aborter(utils.AbortType.NODES, self._params.get('number'))
        else:
            self._abort_checker = utils.Aborter(utils.AbortType.TIME, self._params.get('number'))
        self._search = search.Search(self._abort_checker, self._params)
        return

    def play(self, game):
        """ Returns the "best" move to play in the current <game>-state and its value, after some
            deliberation (<check_abort>).
        """
        return self._search.best_move(game)
