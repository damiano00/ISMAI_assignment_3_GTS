import agents.mm_based_agent as mm_based_agent
import ab_search as search


class ABAgent(mm_based_agent.MMBasedAgent):


    # -------------- Evaluation functions -----------------------

    @staticmethod
    def evaluate_enhanced(game):
        #  TODO: Your task is to implement this function (hint: model it on corresponding method in mm_search.py)
        ...
        return 0

    # -------------- Simple move-ordering functions  -----------------------


    def __init__(self, name, params):
        super().__init__(params, f'ab_agent_{name}')
        self._evaluators_list.append(self.evaluate_enhanced)
        self._evaluator = self.get_evaluator(self._params.get('eval', 0), self._evaluators_list)
        self._search = search.Search(self._abort_checker, self._order_moves, self._evaluator, self._params)
        return

    def play(self, game):
        """ Returns the "best" move to play in the current <game>-state and its value, after some
            deliberation (<check_abort>).
        """
        return self._search.best_move(game)
