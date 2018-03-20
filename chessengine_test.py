import unittest

from chessengine import *


class MockBoard:
    board = BoardLike([
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), NoPiece(), NoPiece(),
        NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), NoPiece(), NoPiece(),
        NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), NoPiece(), NoPiece(),
        NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), NoPiece(), NoPiece(),
        NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), NoPiece(), NoPiece(),
        NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), NoPiece(), NoPiece(),
        NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), NoPiece(), NoPiece(),
        NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), NoPiece(), NoPiece(),
        NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(), NoPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
        OutOfBoundsPiece(), OutOfBoundsPiece(), OutOfBoundsPiece(),
    ])

    def __init__(self):
        self.board = MockBoard.board

    def resetboard(self):
        self.board = MockBoard.board


class SquareTest(unittest.TestCase):

    def test_eq(self):
        self.assertTrue(Square('a1') == Square('a1'))
        self.assertFalse(Square('a1') == Square('a2'))

    def test_init(self):
        self.assertEqual(Square('a8').index, 48)
        self.assertEqual(Square('h1').index, 48 + 7 * 15 + 7)
        self.assertEqual(Square(Square('a1')), Square('a1'))

    def test_arithmetic(self):
        self.assertEqual(Square('a8') + 1, Square('a8').index + 1)
        self.assertEqual(Square('a8') + Square('b5'), Square('a8').index + Square('b5').index)
        self.assertEqual(Square('a8') - 1, Square('a8').index - 1)
        self.assertEqual(Square('a8') - Square('b5'), Square('a8').index - Square('b5').index)


class BoardLikeTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.bl = BoardLike(range(225))

    def test_getitem(self):
        self.assertEqual(self.bl[0], 0)
        self.assertEqual(self.bl[224], 224)
        self.assertEqual(self.bl[Square('a8')], Square('a8').index)

    def test_replace(self):
        newboard = self.board.replace(Square('a1'), 0)
        self.assertEqual(newboard[Square('a1')], 0)


class BoardTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.board = Board(self.board._board).replace(Square('a1'), Rook(Side.WHITE)) \
            .replace(Square('c5'), Pawn(Side.WHITE))

    def test_attacked(self):
        self.assertTrue(self.board.attacked(Square('a8'), Side.WHITE))
        self.assertTrue(self.board.attacked(Square('d6'), Side.WHITE))
        self.assertTrue(self.board.attacked(Square('b6'), Side.WHITE))

    def test_movepiece(self):
        self.board._movepiece(Square('a1'), Square('a8'))
        self.assertEqual(self.board['a8'].kind, Rook)

    def test_removepiece(self):
        self.board._removepiece(Square('a1'))
        self.assertEqual(self.board['a1'].kind, NoPiece)

    def test_addpiece(self):
        self.board._addpiece(King(Side.WHITE), 'b7')
        self.assertEqual(self.board['b7'].kind, King)


class RookTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.rook = Rook(Side.WHITE)

    def test_attacks(self):
        fromsq = Square('b7')
        for sq in ('b8', 'b6', 'b5', 'b4', 'b3', 'b2', 'b1', 'a7',
                   'c7', 'd7', 'e7', 'f7', 'g7', 'h7'):
            self.assertTrue(
                self.rook.attacks(fromsq, Square(sq), self.board.replace(fromsq, self.rook)))


class BishopTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.bishop = Bishop(Side.WHITE)

    def test_attacks(self):
        fromsq = Square('b7')
        for sq in ('a8', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1', 'c8',
                   'a6'):
            self.assertTrue(
                self.bishop.attacks(fromsq, Square(sq), self.board.replace(fromsq, self.bishop)))


class QueenTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.queen = Queen(Side.WHITE)

    def test_attacks(self):
        fromsq = Square('b7')
        for sq in ('a8', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1', 'c8',
                   'a6', 'b8', 'b6', 'b5', 'b4', 'b3', 'b2', 'b1', 'a7',
                   'c7', 'd7', 'e7', 'f7', 'g7', 'h7'):
            self.assertTrue(
                self.queen.attacks(fromsq, Square(sq), self.board.replace(fromsq, self.queen)))


