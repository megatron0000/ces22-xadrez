from minimax.AI import Minimax
from time import sleep
from chessengine import Pawn, King, Rook, Bishop, Queen, Knight, NoPiece, OutOfBoundsPiece, Square
import signal


PIECE_CODES = {
    Pawn: 'P', King: 'K', Rook: 'R', Bishop: 'B',
    Queen: 'Q', Knight: 'N', NoPiece: '', OutOfBoundsPiece: ''
}


def move2str(move):
    return Square(move.fromsq).name + Square(move.tosq).name + PIECE_CODES[
        NoPiece if move.promotion is None else move.promotion.kind]


def aiprocess(pipe, game):

    ai = Minimax(game)
    terminated = False

    def terminate(*args):
        nonlocal terminated
        terminated = True

    signal.signal(signal.SIGTERM, terminate)

    while not terminated:
        sleep(0.5)
        if pipe.poll():
            game.make(pipe.recv())
            mymove = move2str(ai.ai_move(2, True))
            game.make(mymove)
            pipe.send(mymove)
