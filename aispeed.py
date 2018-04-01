from chessengine import *
from minimax.AI import Minimax
import cProfile

stdgame = [Rook(Side.BLACK), Knight(Side.BLACK), Bishop(Side.BLACK), Queen(Side.BLACK), King(Side.BLACK),
           Bishop(Side.BLACK), Knight(Side.BLACK), Rook(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK),
           Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK), Pawn(Side.BLACK),
           Pawn(Side.BLACK), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
           NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
           NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
           NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
           NoPiece(), Pawn(Side.BLACK), Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE),
           Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE), Pawn(Side.WHITE), Rook(Side.WHITE),
           Knight(Side.WHITE), Bishop(Side.WHITE), Queen(Side.WHITE), King(Side.WHITE), Bishop(Side.WHITE),
           Knight(Side.WHITE), Rook(Side.WHITE)]

game = Game(stdgame, {Side.WHITE: (True, True), Side.BLACK: (True, True)}, None, Side.WHITE)

ai = Minimax(game)


cProfile.run('ai.ai_move(3, True)', 'aispeed.pstats')
