from misc.utils import MaxDepth, Infinity, Loss, NoMove
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

        def alpha_beta(game, ply, depth, pv, state, alpha, beta):
            """ fail-soft alpha-beta search """
            assert(ply >= 0)
            nonlocal nodes, do_abort
            nodes += 1
            if state.is_terminal():
                return Loss + ply
            elif depth <= 0:
                return self._evaluator(game)
            elif self._abort_checker.do_abort(0, nodes):
                do_abort = True
                return 0
            if state.is_terminal() or depth <= 0:
                return self._evaluator(state)
            self._pv.set_none(ply)
            best_value = -Infinity
            moves = self._generate_ordered_moves(ply, game, pv[ply] if ply < len(pv) else NoMove)

            for move in moves:
                state.make(move)
                value = -alpha_beta(game, ply, depth - 1, pv[ply], state, -beta, -alpha)
                state.retract(move)
                best_value = max(value, best_value)
                if do_abort:
                    break
                if best_value > alpha:
                    alpha = best_value
                    self._pv.set(ply, move)
                    if alpha >= beta:
                        break
            return best_value

        self._abort_checker.reset()
        nodes, do_abort = 0, False
        pv_list = []
        for d in range(1, MaxDepth + 1):
            pv_list = self._pv.get_pv()
            v = alpha_beta(game, 0, d, pv_list, game.get_state(), -Infinity, Infinity)
            if self._params.get('verbose', 0) > 0:
                print(d, v, ' ', end='')
                for m in self._pv.get_pv():
                    print(game.get_board().move_to_str(m), end=' ')
                print()
            if do_abort or self._abort_checker.do_abort(d + 1, nodes):
                break
        best_move = self._pv.get(0) if self._pv.get(0) != NoMove else pv_list[0]
        return best_move
