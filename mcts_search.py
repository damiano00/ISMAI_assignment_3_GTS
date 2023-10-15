import random
import copy
import misc.utils as utils
import misc.tree as tree


class NodeLabel:

    def __init__(self, moves):
        self.moves = moves
        self.len = len(self.moves)
        self.n = 0
        self.q = [utils.Avg() for _ in range(self.len)]
        return


class Search:

    # -------------- Simple evaluation functions -----------------------
    @staticmethod
    def playout_policy_0(game):
        # Select a move uniformly at random.
        return random.choice(game.generate())

    def playout_policy_1(self, game):
        # Play a capture move, if one exists, otherwise a random move.
        capture_moves, moves = [], game.generate()
        player = game.get_to_move()
        for m in moves:
            if m[2] != game.get_board().NoPce:
                capture_moves.append(m)
        return random.choice(capture_moves) if capture_moves else random.choice(moves)

    def playout_policy_2(self, game):
        # TODO: Some advanced policy you want to implement
        ...
        return random.choice(game.generate())

    # -------------- Methods -----------------------

    def __init__(self, abort_checker, params):
        self._abort_checker = abort_checker
        self._params = params
        self._tree = None
        eval_level = self._params.get('eval', 0)
        if eval_level == 2:
            self._playout_policy = self.playout_policy_2
        elif eval_level == 1:
            self._playout_policy = self.playout_policy_1
        else:
            self._playout_policy = self.playout_policy_0

    def best_move(self, game):

        def display(depth, label, parent_label, i):
            for _ in range(depth):
                print('  ', end='')
            if parent_label is not None:
                print(parent_label.moves[i], parent_label.q[i].n, parent_label.q[i].avg, end=': ')
            print(label.n)
            return

        def select(node_id):
            # TODO: Modify to use UCT for action selection.
            ...
            node_label = self._tree.node_label(node_id)
            max_i = random.randint(0, len(node_label.moves) - 1)
            return max_i, node_label.moves[max_i]

        def playout(game):
            g = copy.deepcopy(game)
            player = g.get_to_move()
            while not g.is_terminal():
                move = self._playout_policy(g)
                g.make(move)
            return -1.0 if g.get_to_move() == player else 1.0

        def expand(node_id):
            node_label = NodeLabel(game.generate(True))
            if node_id is None:
                node_id = self._tree.add_root(node_label)
            else:
                node_id = self._tree.add_child(node_id, node_label)
            return node_id

        def backup_update(node_id, i, value):
            label = self._tree.node_label(node_id)
            label.n += 1
            label.q[i].add(value)
            return

        def traverse(depth, node_id, parent_id):
            if node_id is None:
                value = playout(game)
                expand(parent_id)
            else:
                if game.is_terminal():
                    value = -1.0  # Loss for player to move.
                else:
                    i, move = select(node_id)
                    game.make(move)
                    value = -traverse(depth + 1, self._tree.child(node_id, i), node_id)
                    game.retract(move)
                    backup_update(node_id, i, value)
            return value

        def simulate():
            traverse(0, self._tree.root(), None)

        def visits(q, i):
            return q[i].n

        self._abort_checker.reset()
        self._tree = tree.Tree()
        nodes = 0
        num_simulations = 0
        while True:
            simulate()
            num_simulations += 1
            if self._abort_checker.do_abort(num_simulations, nodes):
                break
        if self._tree.root() is None:
            expand(self._tree.root())
        node_label = self._tree.node_label(self._tree.root())
        max_i = utils.argmax(node_label.q, len(node_label.q), visits)
        if self._params.get('verbose', 0) > 0:
            print(num_simulations, max_i, node_label.q)

        # tree.depth_first_traversal(self._tree, self._tree.root(), 0, display)  # For debugging purposes.
        return node_label.moves[max_i]
