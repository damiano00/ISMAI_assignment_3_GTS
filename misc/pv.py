#
# Keep track of the principal variation (best line of play by both sides)
#
from misc.utils import NoMove

class PV:

    def __init__(self, max_ply):
        self.max_ply = max_ply
        self.pv = [[NoMove] * (self.max_ply + 1) for _ in range(self.max_ply + 1)]

    def clear(self):
        for i in range(self.max_ply + 1):
            for j in range(self.max_ply + 1):
                self.pv[i][j] = NoMove

    def set_none(self, ply):
        assert ply < self.max_ply
        self.pv[ply][ply] = NoMove
        self.pv[ply+1][ply+1] = NoMove

    def set(self, ply, move):
        assert ply < self.max_ply
        for i in range(ply + 1, self.max_ply + 1):
            self.pv[ply][i] = self.pv[ply + 1][i]
        self.pv[ply][ply] = move

    def get(self, ply):
        assert ply < self.max_ply
        return self.pv[0][ply]

    def get_pv(self):
        moves = []
        for i in range(self.max_ply):
            move = self.get(i)
            if move == NoMove:
                break
            moves.append(move)
        return moves

