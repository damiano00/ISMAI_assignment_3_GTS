from abc import ABC
import agents.agent as agent
import misc.utils as utils


class MMBasedAgent(agent.Agent, ABC):

    # -------------- Simple evaluation functions -----------------------
    @staticmethod
    def evaluate_zero(_):
        return 0

    @staticmethod
    def evaluate_material(game):
        pieces = game.get_pce_count()
        if game.get_to_move() == game.White:
            return pieces[game.White] - pieces[game.Black]
        else:
            return pieces[game.Black] - pieces[game.White]

    # -------------- Simple move-ordering functions  -----------------------
    @staticmethod
    def order_moves_first_captures_noncaptures(ply, game, fmove):
        first, captures, non_captures = [], [], []
        for m in game.generate(ply == 0):  # Shuffle moves on first ply (to improve variability in game play)
            if m == fmove:  # Place move first in ordered list, if exists.
                first.append(m)
            elif m[2] != game.get_board().NoPce:  # capture move
                captures.append(m)
            else:
                non_captures.append(m)
        return first + captures + non_captures

    # -------------- Helper methods  ----------------------
    def get_evaluator(self, num_eval, evaluators):
        if 0 <= num_eval < len(evaluators):
            return evaluators[num_eval]
        else:
            print(f'Warning: ({self._name}) evaluator not available, default to evaluate_zero.')
            return self.evaluate_zero

    # -------------- Class methods  -----------------------

    def __init__(self, params, name):
        super().__init__(params, name)
        self._evaluators_list = [self.evaluate_zero, self.evaluate_material]
        self._evaluator = self.get_evaluator(0, self._evaluators_list)
        self._order_moves = self.order_moves_first_captures_noncaptures
        abort_type = self._params.get('abort')
        if abort_type == 'iterations':
            self._abort_checker = utils.Aborter(utils.AbortType.ITERATIONS, self._params.get('number'))
        elif abort_type == 'nodes':
            self._abort_checker = utils.Aborter(utils.AbortType.NODES, self._params.get('number'))
        else:
            self._abort_checker = utils.Aborter(utils.AbortType.TIME, self._params.get('number'))
        return
