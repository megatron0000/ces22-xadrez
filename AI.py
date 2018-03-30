from chessengine import *


class Minimax:
    class EvalPiece:

        def __init__(self):
            self.pawnWhite = BoardLike(([None] * 15) * 3 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] + [None] * 4 +
                                       [None] * 3 + [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0] + [None] * 4 +
                                       [None] * 3 + [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0] + [None] * 4 +
                                       [None] * 3 + [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5] + [None] * 4 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0] + [None] * 4 +
                                       [None] * 3 + [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5] + [None] * 4 +
                                       [None] * 3 + [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5] + [None] * 4 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] + [None] * 4 +
                                       ([None] * 15) * 4)

            self.pawnBlack = BoardLike(([None] * 15) * 3 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] + [None] * 4 +
                                       [None] * 3 + [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5] + [None] * 4 +
                                       [None] * 3 + [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5] + [None] * 4 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0] + [None] * 4 +
                                       [None] * 3 + [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5] + [None] * 4 +
                                       [None] * 3 + [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0] + [None] * 4 +
                                       [None] * 3 + [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0] + [None] * 4 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] + [None] * 4 +
                                       ([None] * 15) * 4)

            self.knight = BoardLike(([None] * 15) * 3 +
                                    [None] * 3 + [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0] + [None] * 4 +
                                    [None] * 3 + [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0] + [None] * 4 +
                                    [None] * 3 + [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0] + [None] * 4 +
                                    [None] * 3 + [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0] + [None] * 4 +
                                    [None] * 3 + [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0] + [None] * 4 +
                                    [None] * 3 + [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0] + [None] * 4 +
                                    [None] * 3 + [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0] + [None] * 4 +
                                    [None] * 3 + [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0] + [None] * 4 +
                                    ([None] * 15) * 4)

            self.bishopWhite = BoardLike(([None] * 15) * 3 +
                                         [None] * 3 + [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0] + [None] * 4 +
                                         [None] * 3 + [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0] + [None] * 4 +
                                         ([None] * 15) * 4)

            self.bishopBlack = BoardLike(([None] * 15) * 3 +
                                         [None] * 3 + [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0] + [None] * 4 +
                                         [None] * 3 + [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0] + [None] * 4 +
                                         [None] * 3 + [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0] + [None] * 4 +
                                         ([None] * 15) * 4)

            self.rookWhite = BoardLike(([None] * 15) * 3 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] + [None] * 4 +
                                       [None] * 3 + [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0] + [None] * 4 +
                                       ([None] * 15) * 4)

            self.rookBlack = BoardLike(([None] * 15) * 3 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5] + [None] * 4 +
                                       [None] * 3 + [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5] + [None] * 4 +
                                       [None] * 3 + [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] + [None] * 4 +
                                       ([None] * 15) * 4)

            self.Queen = BoardLike(([None] * 15) * 3 +
                                   [None] * 3 + [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0] + [None] * 4 +
                                   [None] * 3 + [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0] + [None] * 4 +
                                   [None] * 3 + [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0] + [None] * 4 +
                                   [None] * 3 + [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5] + [None] * 4 +
                                   [None] * 3 + [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5] + [None] * 4 +
                                   [None] * 3 + [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0] + [None] * 4 +
                                   [None] * 3 + [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0] + [None] * 4 +
                                   [None] * 3 + [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0] + [None] * 4 +
                                   ([None] * 15) * 4)

            self.kingWhite = BoardLike(([None] * 15) * 3 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       [None] * 3 + [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0] + [None] * 4 +
                                       [None] * 3 + [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0] + [None] * 4 +
                                       [None] * 3 + [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0] + [None] * 4 +
                                       [None] * 3 + [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0] + [None] * 4 +
                                       ([None] * 15) * 4)

            self.kingBlack = BoardLike(([None] * 15) * 3 +
                                       [None] * 3 + [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0] + [None] * 4 +
                                       [None] * 3 + [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0] + [None] * 4 +
                                       [None] * 3 + [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0] + [None] * 4 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       [None] * 3 + [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0] + [None] * 4 +
                                       ([None] * 15) * 4)

    def __init__(self, game):

        self.game = game
        self.eval = self.EvalPiece()

    def ai_move(self, depth, is_maximizing_player):
        new_game_moves = self.game.moves()
        best_move_found = None
        position_count = 0
        best_move = -9999
        for move in new_game_moves:
            self.game.make(move)
            value = self._minimax(depth - 1, -10000, 10000, not is_maximizing_player, position_count)
            self.game.unmake()
            if value >= best_move:
                best_move = value
                best_move_found = move
        return best_move_found

    def _minimax(self, depth, alpha, beta, is_maximizing_player, position_count):
        position_count += 1
        new_game_moves = self.game.moves()
        if depth == 0:
            return -self._evaluate_board()
        if is_maximizing_player:
            best_move = -9999
            for move in new_game_moves:
                self.game.make(move)
                best_move = max(
                    best_move,
                    self._minimax(depth - 1, alpha, beta, not is_maximizing_player, position_count))
                self.game.unmake()
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    return best_move
            return best_move
        else:
            best_move = 9999
            for move in new_game_moves:
                self.game.make(move)
                best_move = min(
                    best_move,
                    self._minimax(depth - 1, alpha, beta, not is_maximizing_player, position_count))
                self.game.unmake()
                beta = min(beta, best_move)
                if beta <= alpha:
                    return best_move
            return best_move

    def _evaluate_board(self):
        total_evaluation = 0
        infoboard = tuple(
            (square, self.game.get(square)) for square in self.game.getboard().occuppied(Side.WHITE))
        for infopiece in infoboard:
            total_evaluation += self._get_piece_value(infopiece)
        infoboard = tuple(
            (square, self.game.get(square)) for square in self.game.getboard().occuppied(Side.BLACK))
        for infopiece in infoboard:
            total_evaluation += self._get_piece_value(infopiece)
        return total_evaluation

    def _get_piece_value(self, infopiece):
        i = infopiece[0]
        piece = infopiece[1]
        # if piece.kind in (OutOfBoundsPiece, NoPiece):
        #     return 0
        if piece.side == Side.WHITE:
            return self._get_absolute_value(i, piece)
        else:
            return -self._get_absolute_value(i, piece)

    def _get_absolute_value(self, i, piece):
        if piece.kind == Pawn:
            if piece.side == Side.WHITE:
                return 10 + self.eval.pawnWhite[i]
            else:
                return 10 + self.eval.pawnBlack[i]

        elif piece.kind == Rook:
            if piece.side == Side.WHITE:
                return 50 + self.eval.rookWhite[i]
            else:
                return 50 + self.eval.rookBlack[i]

        elif piece.kind == Knight:
            return 30 + self.eval.knight[i]

        elif piece.kind == Bishop:
            if piece.side == Side.WHITE:
                return 30 + self.eval.bishopWhite[i]
            else:
                return 30 + self.eval.bishopBlack[i]
        elif piece.kind == Queen:
            return 90 + self.eval.Queen[i]
        else:
            if piece.side == Side.WHITE:
                return 900 + self.eval.kingWhite[i]
            else:
                return 900 - self.eval.kingWhite[i]
