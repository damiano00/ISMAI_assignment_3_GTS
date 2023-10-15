from misc.utils import MaxDepth
import misc.pv as pv
import random

class Search:

    def __init__(self, abort_checker, ordered_moves, evaluator, params):
        self._abort_checker = abort_checker
        self._generate_ordered_moves = ordered_moves
        self._evaluator = evaluator
        self._params = params
        self._pv = pv.PV(MaxDepth)

    def best_move(self, game):
        # TODO: Your task is to implement this function (hint: model it on corresponding method in mm_search.py)
        return random.choice(game.generate())
