from chessengine import*
from guiengine import*
from Interfaces import*
from enum import Enum


class Minimax:

    class EvalPiece:

        def __init__(self):
            self.pawnWhite = ([None] * 15) * 3 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) + [None] * 4 + \
                             [None] * 3 + (5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0) + [None] * 4 + \
                             [None] * 3 + (1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0) + [None] * 4 + \
                             [None] * 3 + (0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5) + [None] * 4 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0) + [None] * 4 + \
                             [None] * 3 + (0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5) + [None] * 4 + \
                             [None] * 3 + (0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5) + [None] * 4 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) + [None] * 4 + \
                             ([None] * 15) * 4

            self.pawnBlack = ([None] * 15) * 3 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) + [None] * 4 + \
                             [None] * 3 + (0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5) + [None] * 4 + \
                             [None] * 3 + (0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5) + [None] * 4 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0) + [None] * 4 + \
                             [None] * 3 + (0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5) + [None] * 4 + \
                             [None] * 3 + (1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0) + [None] * 4 + \
                             [None] * 3 + (5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0) + [None] * 4 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) + [None] * 4 + \
                             ([None] * 15) * 4

            self.knight = ([None] * 15) * 3 + \
                          [None] * 3 + (-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0) + [None] * 4 + \
                          [None] * 3 + (-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0) + [None] * 4 + \
                          [None] * 3 + (-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0) + [None] * 4 + \
                          [None] * 3 + (-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0) + [None] * 4 + \
                          [None] * 3 + (-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0) + [None] * 4 + \
                          [None] * 3 + (-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0) + [None] * 4 + \
                          [None] * 3 + (-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0) + [None] * 4 + \
                          [None] * 3 + (-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0) + [None] * 4 + \
                          ([None] * 15) * 4

            self.bishopWhite = ([None] * 15) * 3 + \
                               [None] * 3 + (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0) + [None] * 4 + \
                               [None] * 3 + (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0) + [None] * 4 + \
                               ([None] * 15) * 4

            self.bishopBlack = ([None] * 15) * 3 + \
                               [None] * 3 + (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0) + [None] * 4 + \
                               [None] * 3 + (-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0) + [None] * 4 + \
                               [None] * 3 + (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0) + [None] * 4 + \
                               ([None] * 15) * 4

            self.rookWhite = ([None] * 15) * 3 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) + [None] * 4 + \
                             [None] * 3 + (0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0) + [None] * 4 + \
                             ([None] * 15) * 4

            self.rookBlack = ([None] * 15) * 3 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5) + [None] * 4 + \
                             [None] * 3 + (0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5) + [None] * 4 + \
                             [None] * 3 + (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) + [None] * 4 + \
                             ([None] * 15) * 4

            self.Queen = ([None] * 15) * 3 + \
                         [None] * 3 + (-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0) + [None] * 4 + \
                         [None] * 3 + (-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0) + [None] * 4 + \
                         [None] * 3 + (-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0) + [None] * 4 + \
                         [None] * 3 + (-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5) + [None] * 4 + \
                         [None] * 3 + (0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5) + [None] * 4 + \
                         [None] * 3 + (-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0) + [None] * 4 + \
                         [None] * 3 + (-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0) + [None] * 4 + \
                         [None] * 3 + (-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0) + [None] * 4 + \
                         ([None] * 15) * 4

            self.kingWhite = ([None] * 15) * 3 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             [None] * 3 + (-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0) + [None] * 4 + \
                             [None] * 3 + (-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0) + [None] * 4 + \
                             [None] * 3 + (2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0) + [None] * 4 + \
                             [None] * 3 + (2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0) + [None] * 4 + \
                             ([None] * 15) * 4

            self.kingBlack = ([None] * 15) * 3 + \
                             [None] * 3 + (2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0) + [None] * 4 + \
                             [None] * 3 + (2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0) + [None] * 4 + \
                             [None] * 3 + (-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0) + [None] * 4 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
                             ([None] * 15) * 4

    def __init__(self, game):

        self.game = game
        self.eval = self.EvalPiece()

    def ai_move (self, depth, isMaximisingPlayer):
        newGameMoves = self.game.moves()
        bestMoveFound = None
        positionCount = 0
        bestMove = -9999
        for (move) in newGameMoves:
            self.game.make(move)
            value = self._minimax(depth - 1, -10000, 10000, not isMaximisingPlayer, positionCount)
            self.game.unmake()
            if value >= bestMove:
                bestMove = value
                bestMoveFound = move
        return bestMoveFound

    def _minimax(self, depth, alpha, beta, isMaximisingPlayer, positionCount):
        positionCount += 1
        newGameMoves = self.game.moves()
        if depth == 0:
            return -self._evaluateBoard()
        if isMaximisingPlayer:
            bestMove = -9999
            for move in newGameMoves:
                self.game.make(move)
                bestMove = max(bestMove, self._minimax(depth - 1, alpha, beta, not isMaximisingPlayer, positionCount))
                self.game.unmake()
                alpha = max(alpha, bestMove)
                if beta <= alpha:
                    return bestMove
            return bestMove
        else:
            bestMove = 9999
            for move in newGameMoves:
                self.game.make(move)
                bestMove = min(bestMove, self._minimax(depth - 1, alpha, beta, not isMaximisingPlayer, positionCount))
                self.game.unmake()
                beta = min(beta, bestMove)
                if beta <= alpha:
                    return bestMove
            return bestMove

    def _evaluateBoard(self):
        totalEvaluation = 0
        infoboard = Enum(self.game.getboard().occupied(Side.WHITE))
        for infopiece in infoboard:
            totalEvaluation += self._getPieceValue(infopiece)
        infoboard = Enum(self.game.getboard().occupied(Side.BLACK))
        for infopiece in infoboard:
            totalEvaluation += self._getPieceValue(infopiece)
        return totalEvaluation

    def _getPieceValue (self, infopiece):
        i = infopiece[0]
        piece = infopiece[1]
        if isinstance (piece,(OutOfBoundsPiece,NoPiece)):
            return 0
        if piece.side == Side.WHITE:
            return self.getAbsoluteValue(i, piece)
        else:
            return -self.getAbsoluteValue(i, piece)

    def getAbsoluteValue(self, i, piece):
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
