from chessengine import*
from guiengine import*
from Interfaces import*
import math


class minimaxRoot:

    def __init__(self,game,isMaximisingPlayer):

        self.newGameMoves = game.moves()
        self.bestMove = -9999
        self.bestMoveFound = None
        self.game = game
        self.isMaximisingPlayer = isMaximisingPlayer

    #for(var i = 0; i < newGameMoves.length; i++) {
    # var newGameMove = newGameMoves[i]
    def makeBestMove (self):
        for (move) in self.newGameMoves:
            # game.ugly_move(newGameMove);
            self.game.make(move)
            #var value = minimax(depth - 1, game, -10000, 10000, !isMaximisingPlayer);
            value = self.minimax(depth - 1, self.game, -10000, 10000,not self.isMaximisingPlayer)
            #game.undo();
            self.game.unmake()
            #if(value >= bestMove):
            if value >= self.bestMove:
                #bestMove = value;
                self.bestMove = value
                #bestMoveFound = newGameMove;
                self.bestMoveFound = move
        #return bestMoveFound
        return self.bestMoveFound

#var minimax = function (depth, game, alpha, beta, isMaximisingPlayer) {
class minimax:

    positionCount = 0

    # var newGameMoves = game.ugly_moves();

    def __init__(self,depth, game, alpha, beta, isMaximisingPlayer):
        self.newGameMoves = game.moves()
        self.depth = depth
        self.game = game
        self.alpha = alpha
        self.beta = beta
        self.isMaximisingPlayer = isMaximisingPlayer
        self.

    #if (depth === 0) {
    #    return -evaluateBoard(game.board());
    #}

    def makeBestMove(self):

        #if (isMaximisingPlayer) {
        if self.isMaximisingPlayer:
            #var bestMove = -9999;
            bestMove = -9999
            #for (var i = 0; i < newGameMoves.length; i++) {
            for move in self.newGameMoves:
                #game.ugly_move(newGameMoves[i]);
                self.game.make(move)
                bestMove = math.(bestMove, minimax(depth - 1, game, alpha, beta, !isMaximisingPlayer));
                game.undo();
                alpha = Math.max(alpha, bestMove);
                if (beta <= alpha) {
                    return bestMove;
                }
            }
            return bestMove;
        } else {
            var bestMove = 9999;
            for (var i = 0; i < newGameMoves.length; i++) {
                game.ugly_move(newGameMoves[i]);
                bestMove = Math.min(bestMove, minimax(depth - 1, game, alpha, beta, !isMaximisingPlayer));
                game.undo();
                beta = Math.min(beta, bestMove);
                if (beta <= alpha) {
                    return bestMove;
                }
            }
            return bestMove;
    }
};

var evaluateBoard = function (board) {
    var totalEvaluation = 0;
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            totalEvaluation = totalEvaluation + getPieceValue(board[i][j], i ,j);
        }
    }
    return totalEvaluation;
};

var reverseArray = function(array) {
    return array.slice().reverse();
};

board = ([None] * 15) * 3
for row in range(8):
    board += [None] * 3 + board_array[8 * row:8 * row + 8] + None * 4
board += ([None] * 15) * 4

pawnEvalWhite = ([None] * 15) * 3 + \
                [None] * 3 + (0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0) + [None] * 4 + \
                [None] * 3 + (5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0) + [None] * 4 + \
                [None] * 3 + (1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0) + [None] * 4 + \
                [None] * 3 + (0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5) + [None] * 4 + \
                [None] * 3 + (0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0) + [None] * 4 + \
                [None] * 3 + (0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5) + [None] * 4 + \
                [None] * 3 + (0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5) + [None] * 4 + \
                [None] * 3 + (0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0) + [None] * 4 + \
                ([None] * 15) * 4

pawnEvalBlack = reverseArray(pawnEvalWhite)

knightEval = ([None] * 15) * 3 + \
              [None] * 3 + (-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0) + [None] * 4 + \
              [None] * 3 + (-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0) + [None] * 4 + \
              [None] * 3 + (-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0) + [None] * 4 + \
              [None] * 3 + (-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0) + [None] * 4 + \
              [None] * 3 + (-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0) + [None] * 4 + \
              [None] * 3 + (-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0) + [None] * 4 + \
              [None] * 3 + (-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0) + [None] * 4 + \
              [None] * 3 + (-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0) + [None] * 4 + \
              ([None] * 15) * 4

bishopEvalWhite = ([None] * 15) * 3 + \
              [None] * 3 + (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0) + [None] * 4 + \
              [None] * 3 + (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0) + [None] * 4 + \
              ([None] * 15) * 4

bishopEvalBlack = reverseArray(bishopEvalWhite)

rookEvalWhite = ([None] * 15) * 3 + \
              [None] * 3 + (0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0) + [None] * 4 + \
              [None] * 3 + (0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5) + [None] * 4 + \
              [None] * 3 + (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5) + [None] * 4 + \
              [None] * 3 + (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5) + [None] * 4 + \
              [None] * 3 + (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5) + [None] * 4 + \
              [None] * 3 + (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5) + [None] * 4 + \
              [None] * 3 + (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5) + [None] * 4 + \
              [None] * 3 + (0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0) + [None] * 4 + \
              ([None] * 15) * 4

rookEvalBlack = reverseArray(rookEvalWhite)

evalQueen = ([None] * 15) * 3 + \
              [None] * 3 + (-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0) + [None] * 4 + \
              [None] * 3 + (-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5) + [None] * 4 + \
              [None] * 3 + (0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0) + [None] * 4 + \
              [None] * 3 + (-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0) + [None] * 4 + \
              [None] * 3 + (-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0) + [None] * 4 + \
              ([None] * 15) * 4

kingEvalWhite = ([None] * 15) * 3 + \
              [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
              [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
              [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
              [None] * 3 + (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0) + [None] * 4 + \
              [None] * 3 + (-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0) + [None] * 4 + \
              [None] * 3 + (-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0) + [None] * 4 + \
              [None] * 3 + (2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0) + [None] * 4 + \
              [None] * 3 + (2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0) + [None] * 4 + \
              ([None] * 15) * 4

kingEvalBlack = reverseArray(kingEvalWhite);




var getPieceValue = function (piece, x, y) {
    if (piece === null) {
        return 0;
    }
    var getAbsoluteValue = function (piece, isWhite, x ,y) {
        if (piece.type === 'p') {
            return 10 + ( isWhite ? pawnEvalWhite[y][x] : pawnEvalBlack[y][x] );
        } else if (piece.type === 'r') {
            return 50 + ( isWhite ? rookEvalWhite[y][x] : rookEvalBlack[y][x] );
        } else if (piece.type === 'n') {
            return 30 + knightEval[y][x];
        } else if (piece.type === 'b') {
            return 30 + ( isWhite ? bishopEvalWhite[y][x] : bishopEvalBlack[y][x] );
        } else if (piece.type === 'q') {
            return 90 + evalQueen[y][x];
        } else if (piece.type === 'k') {
            return 900 + ( isWhite ? kingEvalWhite[y][x] : kingEvalBlack[y][x] );
        }
        throw "Unknown piece type: " + piece.type;
    };

    var absoluteValue = getAbsoluteValue(piece, piece.color === 'w', x ,y);
    return piece.color === 'w' ? absoluteValue : -absoluteValue;
};