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

    def test_plmoves(self):
        context = Context(
            {Side.WHITE: Square('a8'), Side.BLACK: Square('a9')},
            {Side.WHITE: False, Side.BLACK: False},
            Square('c6'))
        self.board = self.board.replace(Square('d5'), Rook(Side.WHITE)) \
            .replace(Square('d3'), Pawn(Side.BLACK))
        moves = Rook(Side.WHITE).plmoves(Square('d5'), self.board, context)
        self.assertEqual(
            sorted(['d6', 'd7', 'd8', 'd4', 'd3', 'c5', 'b5', 'a5', 'e5', 'f5', 'g5', 'h5']),
            sorted([Square(i.tosq).name for i in moves]))
        self.assertTrue(Move(Square('d5'), Square('d3'), MoveKind.CAPTURE, None) in moves)


class BishopTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.bishop = Bishop(Side.WHITE)

    def test_attacks(self):
        fromsq = Square('b7')
        for sq in ('a8', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1', 'c8',
                   'a6'):
            self.assertTrue(
                self.bishop.attacks(fromsq, Square(sq), self.board.replace(fromsq, self.bishop)))

    def test_plmoves(self):
        context = Context(
            {Side.WHITE: Square('a8'), Side.BLACK: Square('a9')},
            {Side.WHITE: False, Side.BLACK: False},
            Square('c6'))
        self.board = self.board.replace(Square('a5'), Bishop(Side.WHITE)) \
            .replace(Square('d8'), Pawn(Side.BLACK))
        moves = Bishop(Side.WHITE).plmoves(Square('a5'), self.board, context)
        self.assertEqual(
            sorted(['b6', 'c7', 'd8', 'b4', 'c3', 'd2', 'e1']),
            sorted([Square(i.tosq).name for i in moves]))
        self.assertTrue(Move(Square('a5'), Square('d8'), MoveKind.CAPTURE, None) in moves)


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

    def test_plmoves(self):
        """
        Ela herda de SlidingPiece, então é fácil ver se funciona vendo se Rook e Bishop
        ambos funcionam
        """
        pass


class KnightTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.knight = Knight(Side.WHITE)
        self.resetboard()

    def test_attacks(self):
        fromsq = Square('b7')
        self.board = self.board.replace(fromsq, self.knight)
        self.assertFalse(self.knight.attacks(fromsq, Square('d7'), self.board))
        self.assertTrue(self.knight.attacks(fromsq, Square('d8'), self.board))

    def test_plmoves(self):
        fromsq = Square('b7')
        self.board = self.board.replace(fromsq, self.knight) \
            .replace(Square('d8'), Pawn(Side.BLACK))
        moves = self.knight.plmoves(fromsq, self.board, None)  # Não precisa de contexto
        self.assertEqual(
            sorted(['d8', 'd6', 'a5', 'c5']),
            sorted([Square(i.tosq).name for i in moves]))
        self.assertTrue(Move(fromsq, Square('d8'), MoveKind.CAPTURE, None) in moves)


class PawnTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.pawn = Pawn(Side.WHITE)
        self.resetboard()

    def test_attacks(self):
        fromsq = Square('b7')
        self.board = self.board.replace(fromsq, self.pawn)
        self.assertFalse(self.pawn.attacks(fromsq, Square('b8'), self.board))
        self.assertTrue(self.pawn.attacks(fromsq, Square('c8'), self.board))

    def test_plmoves(self):
        fromsq = Square('b7')
        self.board = self.board.replace(fromsq, self.pawn) \
            .replace(Square('c8'), Pawn(Side.BLACK))
        moves = self.pawn.plmoves(fromsq, self.board, Context(None, None, Square('e7')))
        self.assertEqual(
            sorted(['b8'] * 4 + ['c8'] * 4),  # 4 promoções, 4 promoções com captura
            sorted([Square(i.tosq).name for i in moves]))
        self.assertTrue(
            Move(fromsq, Square('c8'), MoveKind.PROMOTION_CAPTURE, Rook(Side.WHITE)) in moves)


class KingTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.king = King(Side.WHITE)
        self.resetboard()
        self.board = Board(self.board._board)

    def test_attacks(self):
        fromsq = Square('e1')
        self.board = self.board.replace(fromsq, self.king)
        self.assertFalse(self.king.attacks(fromsq, Square('b8'), self.board))
        self.assertTrue(self.king.attacks(fromsq, Square('d2'), self.board))

    def test_plmoves(self):
        fromsq = Square('e1')
        self.board = self.board.replace(fromsq, self.king) \
            .replace(Square('e2'), Pawn(Side.BLACK))
        moves = self.king.plmoves(fromsq, self.board, Context(None, {
            Side.BLACK: None,
            Side.WHITE: (True, True)
        }, None))
        self.assertEqual(
            sorted(['d1', 'd2', 'e2', 'f2', 'f1']),  # Peão bloqueia castle
            sorted([Square(i.tosq).name for i in moves]))
        self.board = self.board.replace(Square('e2'), NoPiece())
        moves = self.king.plmoves(fromsq, self.board, Context(None, {
            Side.BLACK: None,
            Side.WHITE: (True, True)
        }, None))
        self.assertEqual(
            sorted(['d1', 'd2', 'e2', 'f2', 'f1', 'g1', 'c1']),  # Agora pode fazer castle
            sorted([Square(i.tosq).name for i in moves]))


class MoveQuietExecutorTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.resetboard()
        self.board = Board(self.board._board)
        self.executor = MoveQuietExecutor()

    def test_exec(self):
        self.board = self.board.replace(Square('a1'), Rook(Side.WHITE))
        antimove = self.executor.exec(
            Move(Square('a1'), Square('a8'), MoveKind.QUIET, None),
            self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['a8'], Rook(Side.WHITE))
        self.assertEqual(self.board['a1'], NoPiece())
        antimove.kind.exec(antimove, self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['a1'], Rook(Side.WHITE))
        self.assertEqual(self.board['a8'], NoPiece())


class MovePawn2ExecutorTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.resetboard()
        self.board = Board(self.board._board)
        self.executor = MoveQuietExecutor()

    def test_exec(self):
        self.board = self.board.replace(Square('a2'), Pawn(Side.WHITE))
        antimove = self.executor.exec(
            Move(Square('a2'), Square('a4'), MoveKind.PAWN2, None),
            self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['a4'], Pawn(Side.WHITE))
        self.assertEqual(self.board['a2'], NoPiece())
        antimove.kind.exec(antimove, self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['a2'], Pawn(Side.WHITE))
        self.assertEqual(self.board['a4'], NoPiece())


class MoveCaptureExecutorTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.resetboard()
        self.board = Board(self.board._board)
        self.executor = MoveCaptureExecutor()

    def test_exec(self):
        self.board = self.board.replace(Square('a1'), Rook(Side.WHITE)) \
            .replace(Square('a8'), Bishop(Side.BLACK))
        antimove = self.executor.exec(
            Move(Square('a1'), Square('a8'), MoveKind.QUIET, None),
            self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['a8'], Rook(Side.WHITE))
        self.assertEqual(self.board['a1'], NoPiece())
        antimove.kind.exec(antimove, self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['a1'], Rook(Side.WHITE))
        self.assertEqual(self.board['a8'], Bishop(Side.BLACK))


class MoveCastleKingExecutorTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.resetboard()
        self.board = Board(self.board._board)
        self.executor = MoveCastleKingExecutor()

    def test_exec(self):
        self.board = self.board.replace(Square('e1'), King(Side.WHITE)) \
            .replace(Square('h1'), Rook(Side.WHITE))
        antimove = self.executor.exec(
            Move(Square('e1'), Square('g1'), MoveKind.CASTLE_KING, None),
            self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['e1'], NoPiece())
        self.assertEqual(self.board['h1'], NoPiece())
        self.assertEqual(self.board['g1'], King(Side.WHITE))
        self.assertEqual(self.board['f1'], Rook(Side.WHITE))
        antimove.kind.exec(antimove, self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['g1'], NoPiece())
        self.assertEqual(self.board['f1'], NoPiece())
        self.assertEqual(self.board['e1'], King(Side.WHITE))
        self.assertEqual(self.board['h1'], Rook(Side.WHITE))


class MoveCastleQueenExecutorTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.resetboard()
        self.board = Board(self.board._board)
        self.executor = MoveCastleQueenExecutor()

    def test_exec(self):
        self.board = self.board.replace(Square('e1'), King(Side.WHITE)) \
            .replace(Square('a1'), Rook(Side.WHITE))
        antimove = self.executor.exec(
            Move(Square('e1'), Square('c1'), MoveKind.CASTLE_QUEEN, None),
            self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['e1'], NoPiece())
        self.assertEqual(self.board['a1'], NoPiece())
        self.assertEqual(self.board['c1'], King(Side.WHITE))
        self.assertEqual(self.board['d1'], Rook(Side.WHITE))
        antimove.kind.exec(antimove, self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['c1'], NoPiece())
        self.assertEqual(self.board['d1'], NoPiece())
        self.assertEqual(self.board['e1'], King(Side.WHITE))
        self.assertEqual(self.board['a1'], Rook(Side.WHITE))


class MoveEpCaptureExecutorTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.resetboard()
        self.board = Board(self.board._board)
        self.executor = MoveEpCaptureExecutor()

    def test_exec(self):
        self.board = self.board.replace(Square('d4'), Pawn(Side.BLACK)) \
            .replace(Square('c4'), Pawn(Side.WHITE))
        antimove = self.executor.exec(
            Move(Square('d4'), Square('c3'), MoveKind.EP_CAPTURE, None),
            self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['d4'], NoPiece())
        self.assertEqual(self.board['e4'], NoPiece())
        self.assertEqual(self.board['c3'], Pawn(Side.BLACK))
        antimove.kind.exec(antimove, self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['c3'], NoPiece())
        self.assertEqual(self.board['c4'], Pawn(Side.WHITE))
        self.assertEqual(self.board['d4'], Pawn(Side.BLACK))


class MovePromotionExecutorTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.resetboard()
        self.board = Board(self.board._board)
        self.executor = MovePromotionExecutor()

    def test_exec(self):
        self.board = self.board.replace(Square('a2'), Pawn(Side.BLACK))
        antimove = self.executor.exec(
            Move(Square('a2'), Square('a1'), MoveKind.PROMOTION, Rook(Side.BLACK)),
            self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['a1'], Rook(Side.BLACK))
        self.assertEqual(self.board['a2'], NoPiece())
        antimove.kind.exec(antimove, self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['a1'], NoPiece())
        self.assertEqual(self.board['a2'], Pawn(Side.BLACK))


class MovePromotionCaptureExecutorTest(unittest.TestCase, MockBoard):

    def setUp(self):
        self.resetboard()
        self.board = Board(self.board._board)
        self.executor = MovePromotionCaptureExecutor()

    def test_exec(self):
        self.board = self.board.replace(Square('a2'), Pawn(Side.BLACK)) \
            .replace(Square('b1'), Queen(Side.WHITE))
        antimove = self.executor.exec(
            Move(Square('a2'), Square('b1'), MoveKind.PROMOTION_CAPTURE, Rook(Side.BLACK)),
            self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['b1'], Rook(Side.BLACK))
        self.assertEqual(self.board['a2'], NoPiece())
        antimove.kind.exec(antimove, self.board._movepiece, self.board._addpiece, self.board._removepiece)
        self.assertEqual(self.board['b1'], Queen(Side.WHITE))
        self.assertEqual(self.board['a2'], Pawn(Side.BLACK))


class GameTest(unittest.TestCase):

    def setUp(self):
        self.board1 = [NoPiece()] * 8 * 7 + [Rook(Side.WHITE)] + [NoPiece()] * 6 + [King(Side.BLACK)]
        self.board2 = [NoPiece()] * 6 + [Rook(Side.BLACK), NoPiece()] + \
                      [NoPiece()] * 8 * 5 + \
                      [Rook(Side.BLACK)] + [NoPiece()] * 7 + \
                      [NoPiece()] * 7 + [King(Side.WHITE)]
        self.board3 = [Bishop(Side.BLACK)] + self.board2[1:]
        self.board4 = [NoPiece()] * 8 + [Pawn(Side.WHITE)] + [NoPiece()] * 7 + [NoPiece()] * 8 * 6
        self.board5 = [NoPiece()] * 8 * 6 + [King(Side.BLACK), NoPiece(), King(Side.WHITE)] + [NoPiece()] * 5 + \
                      [NoPiece()] * 6 + [Rook(Side.BLACK), Bishop(Side.WHITE)]

        self.default_castle = {
            Side.WHITE: (False, False),
            Side.BLACK: (False, False)
        }


    def test_init(self):
        game = Game(self.board1, self.default_castle, None, Side.BLACK)


    def test_check(self):
        game1 = Game(self.board1, self.default_castle, None, Side.BLACK)
        self.assertTrue(game1.check())
        game2 = Game(self.board2, self.default_castle, None, Side.WHITE)
        self.assertFalse(game2.check())
        game3 = Game(self.board3, self.default_castle, None, Side.WHITE)
        self.assertTrue(game3.check())


    def test_stalemate(self):
        game1 = Game(self.board1, self.default_castle, None, Side.BLACK)
        self.assertFalse(game1.stalemate())
        game2 = Game(self.board2, self.default_castle, None, Side.WHITE)
        self.assertTrue(game2.stalemate())
        game3 = Game(self.board3, self.default_castle, None, Side.WHITE)
        self.assertFalse(game3.stalemate())


    def test_checkmate(self):
        game1 = Game(self.board1, self.default_castle, None, Side.BLACK)
        self.assertFalse(game1.checkmate())
        game2 = Game(self.board2, self.default_castle, None, Side.WHITE)
        self.assertFalse(game2.checkmate())
        game3 = Game(self.board3, self.default_castle, None, Side.WHITE)
        self.assertTrue(game3.checkmate())


    def test_make(self):
        game1 = Game(self.board1, self.default_castle, None, Side.BLACK)
        game1.make("h1h2")
        self.assertEqual(game1.get("h2"), King(Side.BLACK))
        game4 = Game(self.board4, self.default_castle, None, Side.WHITE)
        game4.make("a7a8Q")
        self.assertEqual(game4.get("a8"), Queen(Side.WHITE))
        game5 = Game(self.board5, self.default_castle, None, Side.BLACK)
        self.assertEqual(game5.get("g1"), Rook(Side.BLACK))
        self.assertEqual(game5.get("h1"), Bishop(Side.WHITE))
        game5.make("g1h1")
        self.assertEqual(game5.get("g1"), NoPiece())
        self.assertEqual(game5.get("h1"), Rook(Side.BLACK))


    def test_unmake(self):
        game1 = Game(self.board1, self.default_castle, None, Side.BLACK)
        game1.make("h1h2")
        game1.unmake()
        self.assertEqual(game1.get("h2"), NoPiece())
        self.assertEqual(game1.get("h1"), King(Side.BLACK))
        game4 = Game(self.board4, self.default_castle, None, Side.WHITE)
        game4.make("a7a8Q")
        game4.unmake()
        self.assertEqual(game4.get("a8"), NoPiece())
        self.assertEqual(game4.get("a7"), Pawn(Side.WHITE))
