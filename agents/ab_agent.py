import agents.mm_based_agent as mm_based_agent
import ab_search as search
from game.breakthrough import Breakthrough


class ABAgent(mm_based_agent.MMBasedAgent):

    # -------------- Evaluation functions -----------------------

    @classmethod
    def find_all_white_pieces_probability_in_triangle_by_row(cls, white_piece2d, all_black_pieces_position2d, last_row,
                                                             last_column):
        # all_black_pieces_position2d = filter(lambda x: x[1] > white_piece2d[1], sorted(all_black_pieces_position2d,
        # key=lambda x: x[1]))
        all_pieces_in_triangle = []
        for row in range(white_piece2d[1] + 1, last_row):
            all_pieces_in_row = len([x for x in all_black_pieces_position2d if x[1] == row])
            max_cols = (row - white_piece2d[1]) * 2 + 1
            # since len rows == len columns, last row == last column
            if max_cols > last_column:
                max_cols = last_column
            all_pieces_in_triangle.append(all_pieces_in_row / max_cols)
        return all_pieces_in_triangle

    @classmethod
    def find_all_black_pieces_probability_in_triangle_by_row(cls, black_piece2d, all_white_pieces_position2d, first_row,
                                                             last_column):
        all_pieces_in_triangle = []
        for row in range(black_piece2d[1] - 1, first_row, -1):
            all_pieces_in_row = len([x for x in all_white_pieces_position2d if x[1] == row])
            max_cols = (black_piece2d[1] - row) * 2 + 1
            if max_cols > last_column:
                max_cols = last_column
            all_pieces_in_triangle.append(all_pieces_in_row / max_cols)
        return all_pieces_in_triangle

    @classmethod
    def evaluate_state_white(cls, state):
        overall_state = 0
        all_white_pieces_position2d = [state.col_row(piece) for piece in state.get_pce_locations(Breakthrough.White)]
        all_black_pieces_position2d = [state.col_row(piece) for piece in state.get_pce_locations(Breakthrough.Black)]
        # all_pieces_position2d = all_white_pieces_position2d + all_black_pieces_position2d
        # Note these two vars are column, row pairs
        for white_piece2d in all_white_pieces_position2d:
            if white_piece2d[1] == state.rows() - 1:
                overall_state += 1000
                continue
            all_pieces_in_triangle = cls.find_all_black_pieces_probability_in_triangle_by_row(
                white_piece2d, all_black_pieces_position2d, state.rows() - 1, state.cols())
            for index, row in enumerate(all_pieces_in_triangle):
                overall_state += (1 - row) * 1/(index + 1) * (white_piece2d[1] + 1) * 10
        return overall_state

    @classmethod
    def evaluate_state_black(cls, state):
        overall_state = 0
        all_white_pieces_position2d = [state.col_row(piece) for piece in state.get_pce_locations(Breakthrough.White)]
        all_black_pieces_position2d = [state.col_row(piece) for piece in state.get_pce_locations(Breakthrough.Black)]
        # all_pieces_position2d = all_white_pieces_position2d + all_black_pieces_position2d
        # Note these two vars are column, row pairs
        for black_piece2d in all_black_pieces_position2d:
            if black_piece2d[1] == 0:
                overall_state += 1000
                continue
            all_pieces_in_triangle = cls.find_all_black_pieces_probability_in_triangle_by_row(
                black_piece2d, all_white_pieces_position2d, 0, state.cols())
            for index, row in enumerate(all_pieces_in_triangle):
                overall_state += (1 - row) * 1/(index + 1) * (state.rows() - black_piece2d[1]) * 10
        return overall_state

    @classmethod
    def evaluate_state(cls, game, state):
        """
        Evaluate the given <state> of the game.
        Victory conditions:
            - Piece in opposite last row (White: board size - row length / Black: row length)
            - No opponent pieces left
            - Opponent has no legal moves (and player has at least 1 legal move)
            -

        """
        if game.get_to_move() == state.White:
            return cls.evaluate_state_white(state)
        return cls.evaluate_state_black(state)

    @staticmethod
    def evaluate_enhanced(game):
        # TODO: Test
        pieces = game.get_pce_count()
        state = game.get_board()
        if game.get_to_move() == game.White:
            return pieces[Breakthrough.White] - pieces[Breakthrough.Black] + ABAgent.evaluate_state(game, state)
        return pieces[Breakthrough.Black] - pieces[Breakthrough.White] + ABAgent.evaluate_state(game, state)

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
