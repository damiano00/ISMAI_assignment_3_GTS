import misc.pv as pv
from game.breakthrough import Breakthrough
from misc.utils import Infinity, Loss, MaxDepth, NoMove


class Search:

    def __init__(self, abort_checker, ordered_moves, evaluator, params):
        self._abort_checker = abort_checker
        self._generate_ordered_moves = ordered_moves
        self._evaluator = evaluator
        self._params = params
        self._pv = pv.PV(MaxDepth)

    def best_move(self, game: Breakthrough):
        """ fail-soft alpha-beta search """
        def alpha_beta(_game: Breakthrough, ply, depth, pv, alpha, beta):
            assert (ply >= 0)
            nonlocal nodes, do_abort
            nodes += 1
            if _game.is_terminal():
                return Loss + ply
            elif depth <= 0:
                return self._evaluator(_game)
            elif self._abort_checker.do_abort(0, nodes):
                do_abort = True
                return 0

            self._pv.set_none(ply)
            moves = self._generate_ordered_moves(ply, _game, pv[ply] if ply < len(pv) else NoMove)
            for move in moves:
                _game.make(move)
                value = -alpha_beta(_game, ply + 1, depth - 1, pv, -beta, -alpha)
                _game.retract(move)
                if value > alpha:
                    alpha = value
                    self._pv.set(ply, move)
                if alpha >= beta:
                    return alpha
                if do_abort:
                    break
            return alpha

        self._abort_checker.reset()
        nodes, do_abort = 0, False
        pv_list = []
        for d in range(1, MaxDepth + 1):
            pv_list = self._pv.get_pv()
            v = alpha_beta(game, 0, d, pv_list, -Infinity, Infinity)
            if self._params.get('verbose', 0) > 0:
                print(d, v, ' ', end='')
                for m in self._pv.get_pv():
                    print(game.get_board().move_to_str(m), end=' ')
                print()
            if do_abort or self._abort_checker.do_abort(d + 1, nodes):
                break
        best_move = self._pv.get(0) if self._pv.get(0) != NoMove else pv_list[0]
        return best_move
