import agents.mm_based_agent as mm_based_agent
import mm_search as search


class MMAgent(mm_based_agent.MMBasedAgent):

    def __init__(self, name, params):
        super().__init__(params, f'mm_agent_{name}')
        self._evaluator = self.get_evaluator(self._params.get('eval', 0), self._evaluators_list)
        self._search = search.Search(self._abort_checker, self._order_moves, self._evaluator, self._params)
        self._tree = None
        return

    def reset(self):
        """ Reset any information kept between play calls. """
        self._tree = None

    def play(self, game):
        """ Returns the "best" move to play in the current <game>-state and its value, after some
            deliberation (<check_abort>).
        """
        return self._search.best_move(game)
