from collections import deque
from collections import namedtuple
from enum import Enum


class Side(Enum):
    WHITE = 0
    BLACK = 1

    def opponent(self):
        if self is Side.WHITE:
            return Side.BLACK
        else:
            return Side.WHITE


def generate_name2index():
    out = {}
    for i in range(225):
        out[('x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l')
            [i % 15] + str(8 - (i - 45) // 15)] = i
    return out


def generate_index2name():
    out = {}
    for name, index in generate_name2index().items():
        out[index] = name
    return out


def generate_non_sentinel():
    out = {}
    indexes = [x for x in range(45, 165) if 2 < x % 15 < 11]
    for i in range(255):
        out[i] = i in indexes
    return out


class Square(object):
    __index2valid = generate_non_sentinel()
    __instance_cache = {}
    __name2index = generate_name2index()
    __index2name = generate_index2name()

    def __new__(cls, descriptor, *args, **kwargs):
        """descriptor pode ser um int, uma string ou outro Square"""
        if cls.__instance_cache.get(descriptor) is not None:
            return cls.__instance_cache[descriptor]
        obj = object.__new__(cls)
        if isinstance(descriptor, int):
            index = descriptor
            valid = cls.__index2valid[index]
            name = cls.__index2name[index]
            rank = int(name[1:])
        else:
            name = descriptor
            index = cls.__name2index[name]
            valid = cls.__index2valid[index]
            rank = int(name[1])
        obj.name = name
        obj.index = index
        obj.rank = rank
        obj.valid = valid
        cls.__instance_cache[name] = obj
        cls.__instance_cache[index] = obj
        cls.__instance_cache[obj] = obj
        return obj

    def __radd__(self, other):
        return self.index + other

    def __add__(self, other):
        return self.index + other

    def __sub__(self, other):
        return self.index - other

    def __rsub__(self, other):
        return other - self.index

    def __eq__(self, other):
        return self.index == Square(other).index

    def __hash__(self):
        return self.index

    def __lt__(self, other):
        return self.index < other

    def __gt__(self, other):
        return self.index > other

    def __repr__(self):
        return '<Square(' + self.name + ')>'


class BoardLike:

    def __init__(self, datalist):
        if len(datalist) != 15 * 15:
            raise ValueError('datalist should be 15*15 in length')
        self._board = datalist

    def __len__(self):
        return len(self._board)

    def __getitem__(self, item):
        return self._board[Square(item).index]

    def __iter__(self):
        return self._board.__iter__()

    def replace(self, square, newcontent):
        copylist = list(self._board)
        copylist[Square(square).index] = newcontent
        return self.__class__(copylist)


class Board(BoardLike):

    def __init__(self, datalist):
        super().__init__(datalist)
        # { [side: Side]: {[key: Square]: bool?} }
        self.__playersquares = {
            Side.WHITE: {},
            Side.BLACK: {}
        }
        # Quadrados dos reis
        self.__kings = {Side.WHITE: None, Side.BLACK: None}
        for sq, piece in enumerate(self._board):
            if Square(sq).valid and piece.side is not None:
                self.__playersquares[piece.side][Square(sq)] = True
                if piece.kind is King:
                    self.__kings[piece.side] = Square(sq)

    def occuppied(self, side):
        return self.__playersquares[side].keys()

    def attacked(self, square, side):
        for fromsq in self.__playersquares[side]:
            if self[fromsq].attacks(fromsq, square, self):
                return True
        return False

    def _movepiece(self, fromsq, tosq):
        fromsq = Square(fromsq)
        tosq = Square(tosq)
        piece = self._board[fromsq.index]
        oldpiece = self._board[tosq.index]
        if oldpiece.kind is not NoPiece:
            self._removepiece(tosq)
        # tabuleiro
        self._board[fromsq.index] = NoPiece()
        self._board[tosq.index] = piece
        # lista de quadrados do jogador
        del self.__playersquares[piece.side][fromsq]
        self.__playersquares[piece.side][tosq] = True
        # lista de reis
        if piece.kind is King:
            self.__kings[piece.side] = tosq
        return oldpiece

    def _addpiece(self, piece, square):
        square = Square(square)
        # tabuleiro
        self._board[square.index] = piece
        # lista de quadrados do jogador
        # print(piece, piece.side, square)
        self.__playersquares[piece.side][square] = True
        # lista de reis
        if piece.kind is King:
            self.__kings[piece.side] = square

    def _removepiece(self, square):
        square = Square(square)
        piece = self._board[square.index]
        side = piece.side
        # tabuleiro
        self._board[square.index] = NoPiece()
        # lista de quadrados do jogador
        del self.__playersquares[side][square]
        # lista de reis
        if piece.kind is King:
            self.__kings[piece.side] = None
        return piece

    def king(self, side):
        return self.__kings[side]


Context = namedtuple('Context', 'kings can_castle ep')

Move = namedtuple('Move', 'fromsq tosq kind promotion')

AntiMove = namedtuple('AntiMove', 'fromsq tosq addpiece addpos kind')


class MoveExecutor:

    def exec(self, move, movepiece, addpiece, removepiece):
        pass


class MoveQuietExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)
        return AntiMove(move.tosq, move.fromsq, None, None, MoveKind.ANTI_QUIET)


class MoveAntiQuietExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)


class MoveEpCaptureExecutor(MoveExecutor):
    # Distância ao quadrado onde está a peça que fez en passant e que vai ser capturada
    __captureoffset = {
        -16: -1,
        -14: +1,
        +14: -1,
        +16: +1
    }

    def exec(self, move, movepiece, addpiece, removepiece):
        middlesq = move.fromsq + self.__captureoffset[move.tosq - move.fromsq]
        captured = movepiece(move.fromsq, middlesq)
        movepiece(middlesq, move.tosq)
        return AntiMove(move.tosq, move.fromsq, captured, middlesq, MoveKind.ANTI_EP_CAPTURE)


class MoveAntiEpCaptureExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)
        addpiece(move.addpiece, move.addpos)


class MovePawn2Executor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)
        return AntiMove(move.tosq, move.fromsq, None, None, MoveKind.ANTI_PAWN2)


class MoveAntiPawn2Executor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)


class MoveCaptureExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        captured = movepiece(move.fromsq, move.tosq)
        return AntiMove(move.tosq, move.fromsq, captured, move.tosq, MoveKind.ANTI_CAPTURE)


class MoveAntiCaptureExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)
        addpiece(move.addpiece, move.addpos)


class MovePromotionExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        pawn = removepiece(move.fromsq)
        addpiece(move.promotion, move.tosq)
        return AntiMove(move.tosq, move.fromsq, pawn, move.fromsq, MoveKind.ANTI_PROMOTION)


class MoveAntiPromotionExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        removepiece(move.fromsq)
        addpiece(move.addpiece, move.addpos)


class MovePromotionCaptureExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        captured = movepiece(move.fromsq, move.tosq)
        addpiece(move.promotion, move.tosq)
        return AntiMove(
            move.tosq, move.fromsq, captured, move.tosq, MoveKind.ANTI_PROMOTION_CAPTURE)


class MoveAntiPromotionCaptureExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        side = removepiece(move.fromsq).side
        addpiece(move.addpiece, move.addpos)
        addpiece(Pawn(side), move.tosq)


class MoveCastleKingExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)
        movepiece(move.tosq + 1, move.fromsq + 1)
        return AntiMove(move.tosq, move.fromsq, None, None, MoveKind.ANTI_CASTLE_KING)


class MoveAntiCastleKingExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)
        movepiece(move.tosq + 1, move.fromsq + 1)


class MoveCastleQueenExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)
        movepiece(move.tosq - 2, move.tosq + 1)
        return AntiMove(move.tosq, move.fromsq, None, None, MoveKind.ANTI_CASTLE_QUEEN)


class MoveAntiCastleQueenExecutor(MoveExecutor):

    def exec(self, move, movepiece, addpiece, removepiece):
        movepiece(move.fromsq, move.tosq)
        movepiece(move.tosq - 1, move.fromsq - 2)


class MoveKind(Enum):
    QUIET = MoveQuietExecutor()
    CAPTURE = MoveCaptureExecutor()
    PAWN2 = MovePawn2Executor()
    EP_CAPTURE = MoveEpCaptureExecutor()
    PROMOTION = MovePromotionExecutor()
    PROMOTION_CAPTURE = MovePromotionCaptureExecutor()
    CASTLE_KING = MoveCastleKingExecutor()
    CASTLE_QUEEN = MoveCastleQueenExecutor()
    ANTI_QUIET = MoveAntiQuietExecutor()
    ANTI_CAPTURE = MoveAntiCaptureExecutor()
    ANTI_PAWN2 = MoveAntiPawn2Executor()
    ANTI_EP_CAPTURE = MoveAntiEpCaptureExecutor()
    ANTI_PROMOTION = MoveAntiPromotionExecutor()
    ANTI_PROMOTION_CAPTURE = MoveAntiPromotionCaptureExecutor()
    ANTI_CASTLE_KING = MoveAntiCastleKingExecutor()
    ANTI_CASTLE_QUEEN = MoveAntiCastleQueenExecutor()

    def exec(self, move, movepiece, addpiece, removepiece):
        return self.value.exec(move, movepiece, addpiece, removepiece)


class Piece(object):
    __instance_cache = {}

    def __new__(cls, side, *args, **kwargs):
        if cls.__instance_cache.get((cls, side)) is None:
            cls.__instance_cache[(cls, side)] = object.__new__(cls)
        return cls.__instance_cache[(cls, side)]

    def __init__(self, side):
        self.side = side
        self.kind = self.__class__

    def attacks(self, fromsq, tosq, board):
        pass

    def plmoves(self, fromsq, board, context):
        pass


class NoPiece(Piece):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, None)

    def __init__(self):
        super().__init__(None)

    def attacks(self, fromsq, tosq, board):
        raise TypeError('There is no piece here. It cannot attack')

    def plmoves(self, fromsq, board, context):
        raise TypeError('There is no piece here. It cannot move')


class OutOfBoundsPiece(Piece):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, None)

    def __init__(self):
        super().__init__(None)

    def attacks(self, fromsq, tosq, board):
        raise TypeError('This piece represents out-of-the-board. It cannot attack')

    def plmoves(self, fromsq, board, context):
        raise TypeError('This piece represents out-of-the-board. It cannot move')


class SlidingPiece(Piece):
    """Subclasses devem preencher rays e directions"""
    rays = None
    directions = None

    def attacks(self, fromsq, tosq, board):
        increment = self.rays[15 * 15 // 2 + fromsq - tosq]
        if increment is None:
            return False
        currsq = tosq + increment
        while board[currsq].kind is NoPiece:
            currsq += increment
        if currsq == fromsq:
            return True
        return False

    def plmoves(self, fromsq, board, context):
        moves = []
        for direction in self.directions:
            currindex = fromsq
            while True:
                currindex += direction
                if board[currindex].kind is OutOfBoundsPiece:
                    break
                elif board[currindex].kind is NoPiece:
                    moves.append(Move(fromsq, currindex, MoveKind.QUIET, None))
                    continue
                elif board[currindex].side is not self.side:
                    moves.append(Move(fromsq, currindex, MoveKind.CAPTURE, None))
                break
        return moves


class Rook(SlidingPiece):
    rays = BoardLike((
        None, None, None, None, None, None, None, -15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, -15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, -15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, -15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, -15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, -15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, -15, None, None, None, None, None, None, None,
        -1, -1, -1, -1, -1, -1, -1, None, 1, 1, 1, 1, 1, 1, 1,
        None, None, None, None, None, None, None, 15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, 15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, 15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, 15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, 15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, 15, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, 15, None, None, None, None, None, None, None
    ))

    directions = (-1, -15, 1, 15)


class Bishop(SlidingPiece):
    rays = BoardLike((
        -16, None, None, None, None, None, None, None, None, None, None, None, None, None, -14,
        None, -16, None, None, None, None, None, None, None, None, None, None, None, -14, None,
        None, None, -16, None, None, None, None, None, None, None, None, None, -14, None, None,
        None, None, None, -16, None, None, None, None, None, None, None, -14, None, None, None,
        None, None, None, None, -16, None, None, None, None, None, -14, None, None, None, None,
        None, None, None, None, None, -16, None, None, None, -14, None, None, None, None, None,
        None, None, None, None, None, None, -16, None, -14, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, 14, None, 16, None, None, None, None, None, None,
        None, None, None, None, None, 14, None, None, None, 16, None, None, None, None, None,
        None, None, None, None, 14, None, None, None, None, None, 16, None, None, None, None,
        None, None, None, 14, None, None, None, None, None, None, None, 16, None, None, None,
        None, None, 14, None, None, None, None, None, None, None, None, None, 16, None, None,
        None, 14, None, None, None, None, None, None, None, None, None, None, None, 16, None,
        14, None, None, None, None, None, None, None, None, None, None, None, None, None, 16,
    ))

    directions = (-16, -14, 16, 14)


class Queen(SlidingPiece):
    rays = BoardLike((
        -16, None, None, None, None, None, None, -15, None, None, None, None, None, None, -14,
        None, -16, None, None, None, None, None, -15, None, None, None, None, None, -14, None,
        None, None, -16, None, None, None, None, -15, None, None, None, None, -14, None, None,
        None, None, None, -16, None, None, None, -15, None, None, None, -14, None, None, None,
        None, None, None, None, -16, None, None, -15, None, None, -14, None, None, None, None,
        None, None, None, None, None, -16, None, -15, None, -14, None, None, None, None, None,
        None, None, None, None, None, None, -16, -15, -14, None, None, None, None, None, None,
        -1, -1, -1, -1, -1, -1, -1, None, 1, 1, 1, 1, 1, 1, 1,
        None, None, None, None, None, None, 14, 15, 16, None, None, None, None, None, None,
        None, None, None, None, None, 14, None, 15, None, 16, None, None, None, None, None,
        None, None, None, None, 14, None, None, 15, None, None, 16, None, None, None, None,
        None, None, None, 14, None, None, None, 15, None, None, None, 16, None, None, None,
        None, None, 14, None, None, None, None, 15, None, None, None, None, 16, None, None,
        None, 14, None, None, None, None, None, 15, None, None, None, None, None, 16, None,
        14, None, None, None, None, None, None, 15, None, None, None, None, None, None, 16,
    ))

    directions = (-1, -16, -15, -14, 1, 16, 15, 14)


class Knight(Piece):
    offsets = (-17, -31, -29, -13, 17, 31, 29, 13)

    def attacks(self, fromsq, tosq, board):
        return tosq - fromsq in self.offsets

    def plmoves(self, fromsq, board, context):
        moves = []
        for offset in self.offsets:
            sq = fromsq + offset
            if board[sq].kind is NoPiece:
                moves.append(Move(fromsq, sq, MoveKind.QUIET, None))
            elif board[sq].kind is not OutOfBoundsPiece and board[sq].side is not self.side:
                moves.append(Move(fromsq, sq, MoveKind.CAPTURE, None))
        return moves


class Pawn(Piece):
    attackoffsets = {
        Side.WHITE: (-16, -14),
        Side.BLACK: (14, 16)
    }

    walkoffset = {
        Side.WHITE: -15,
        Side.BLACK: 15
    }

    initialrank = {
        Side.WHITE: 2,
        Side.BLACK: 7
    }

    def attacks(self, fromsq, tosq, board):
        return tosq - fromsq in self.attackoffsets[self.side]

    def plmoves(self, fromsq, board, context):
        moves = []
        canpromote = False
        # Double move
        if Square(fromsq).rank == self.initialrank[self.side] \
                and board[fromsq + self.walkoffset[self.side]].kind is NoPiece \
                and board[fromsq + 2 * self.walkoffset[self.side]].kind is NoPiece:
            moves.append(
                Move(fromsq, fromsq + 2 * self.walkoffset[self.side], MoveKind.PAWN2, None))
        # Promotion without capture
        if Square(fromsq).rank == self.initialrank[self.side.opponent()] \
                and board[fromsq + self.walkoffset[self.side]].kind is NoPiece:
            for piece in (Queen(self.side), Rook(self.side), Bishop(self.side), Knight(self.side)):
                moves.append(
                    Move(fromsq, fromsq + self.walkoffset[self.side], MoveKind.PROMOTION, piece))
            canpromote = True
        # En passant capture
        if context.ep is not None and context.ep - fromsq in self.attackoffsets[self.side]:
            moves.append(Move(fromsq, context.ep, MoveKind.EP_CAPTURE, None))
        # Normal move
        if not canpromote and board[fromsq + self.walkoffset[self.side]].kind is NoPiece:
            moves.append(Move(fromsq, fromsq + self.walkoffset[self.side], MoveKind.QUIET, None))
        # Capture and maybe promotion
        for attackoffset in self.attackoffsets[self.side]:
            if board[fromsq + attackoffset].kind is not NoPiece \
                    and board[fromsq + attackoffset].kind is not OutOfBoundsPiece \
                    and board[fromsq + attackoffset].side is not self.side:
                if Square(fromsq).rank == self.initialrank[self.side.opponent()]:
                    for promotion in (Queen(self.side),
                                      Rook(self.side), Bishop(self.side), Knight(self.side)):
                        moves.append(Move(
                            fromsq,
                            fromsq + attackoffset,
                            MoveKind.PROMOTION_CAPTURE,
                            promotion))
                else:
                    moves.append(Move(fromsq, fromsq + attackoffset, MoveKind.CAPTURE, None))
                pass

        return moves


class King(Piece):
    offsets = (-1, -16, -15, -14, 1, 16, 15, 14)

    def attacks(self, fromsq, tosq, board):
        return tosq - fromsq in self.offsets

    def plmoves(self, fromsq, board, context):
        moves = []
        # Quiet and capture moves
        for offset in self.offsets:
            if board[fromsq + offset].kind is NoPiece:
                moves.append(Move(fromsq, fromsq + offset, MoveKind.QUIET, None))
            elif board[fromsq + offset].kind is not OutOfBoundsPiece \
                    and board[fromsq + offset].side is not self.side:
                moves.append(Move(fromsq, fromsq + offset, MoveKind.CAPTURE, None))
        # Castling queen
        if context.can_castle[self.side][0] \
                and board[fromsq - 1].kind is NoPiece \
                and board[fromsq - 2].kind is NoPiece \
                and board[fromsq - 3].kind is NoPiece \
                and not board.attacked(fromsq, self.side.opponent()) \
                and not board.attacked(fromsq - 1, self.side.opponent()) \
                and not board.attacked(fromsq - 2, self.side.opponent()):
            moves.append(Move(fromsq, fromsq - 2, MoveKind.CASTLE_QUEEN, None))
        # Castling king
        if context.can_castle[self.side][1] \
                and board[fromsq + 1].kind is NoPiece \
                and board[fromsq + 2].kind is NoPiece \
                and not board.attacked(fromsq, self.side.opponent()) \
                and not board.attacked(fromsq + 1, self.side.opponent()) \
                and not board.attacked(fromsq + 2, self.side.opponent()):
            moves.append(Move(fromsq, fromsq + 2, MoveKind.CASTLE_KING, None))
        return moves


class Game:
    class GameBoard(Board):

        def movepiece(self, fromsq, tosq):
            return self._movepiece(fromsq, tosq)

        def addpiece(self, piece, square):
            return self._addpiece(piece, square)

        def removepiece(self, square):
            return self._removepiece(square)

    Snapshot = namedtuple('Snapshot', 'turn can_castle ep antimove')

    initialrank = {
        Side.WHITE: '1',
        Side.BLACK: '8'
    }

    def __init__(self, board_array, castle_rights, ep_square, turn):
        if len(board_array) != 64:
            raise ValueError('Can only construct a Game with a 8 * 8 array')
        if OutOfBoundsPiece in [x.kind for x in board_array]:
            raise ValueError('Cannot construct a game board with OutOfBoundsPiece in the middle')
        board = ([OutOfBoundsPiece()] * 15) * 3
        for row in range(8):
            board += [OutOfBoundsPiece()] * 3 + board_array[8 * row:8 * row + 8] + \
                     [OutOfBoundsPiece()] * 4
        board += ([OutOfBoundsPiece()] * 15) * 4
        self.__board = self.GameBoard(board)
        self.__context = Context({
            Side.WHITE: self.__board.king(Side.WHITE),
            Side.BLACK: self.__board.king(Side.BLACK)
        }, castle_rights, ep_square)
        self.__turn = turn
        self.__history = deque()

    def turn(self):
        return self.__turn

    def get(self, square):
        if Square(square).valid is False:
            raise ValueError('Square named ' + Square(square).name +
                             'is not a valid chessboard position')
        return self.__board[square]

    def check(self):
        return self.__board.attacked(self.__board.king(self.__turn), self.__turn.opponent())

    def moves(self, square=None):
        if square is None:
            moves = []
            for square in self.__board.occuppied(self.__turn):
                moves += self.moves(square)
            return moves
        if self.__board[square].side is not self.__turn:
            return []
        legalmoves = []
        piece = self.__board[square]
        moves = piece.plmoves(square, self.__board, self.__context)
        # print(moves)
        for move in moves:
            antimove = move.kind.exec(
                move, self.__board.movepiece, self.__board.addpiece, self.__board.removepiece)
            if not self.check():
                legalmoves.append(move)
            antimove.kind.exec(
                antimove, self.__board.movepiece, self.__board.addpiece, self.__board.removepiece)
        return legalmoves

    def checkmate(self):
        if not self.check():
            return False
        return self.moves() == []

    def stalemate(self):
        if self.check():
            return False
        return self.moves() == []

    def make(self, move):
        if isinstance(move, str):
            fromsq = Square(move[0:2])
            tosq = Square(move[2:4])
            side = self.__board[fromsq].side
            promotion = {
                'N': Knight(side), 'R': Rook(side), 'Q': Queen(side), 'B': Bishop(side)
            }[move[4]] if \
                len(move) == 5 else None
            existent = [x for x in self.__board[fromsq].plmoves(fromsq, self.__board, self.__context)
                        if x.tosq == tosq and x.promotion == promotion]
            move = existent[0]
        antimove = move.kind.exec(
            move, self.__board.movepiece, self.__board.addpiece, self.__board.removepiece)
        if self.check() or self.__board[move.tosq].side is not self.__turn:
            antimove.kind.exec(
                antimove, self.__board.movepiece, self.__board.addpiece, self.__board.removepiece)
            raise RuntimeError('Tried to execute illegal move: ' + str(move))
        self.__history.append(self.Snapshot(self.__turn, {
            Side.WHITE: self.__context.can_castle[Side.WHITE],
            Side.BLACK: self.__context.can_castle[Side.BLACK]
        }, self.__context.ep, antimove))
        # castling
        kind = self.__board[move.tosq].kind
        if kind is King:
            self.__context.can_castle[self.__turn] = (False, False)
        # queen side
        elif self.__context.can_castle[self.__turn][0] and Square(move.fromsq) == Square(
                'a' + self.initialrank[self.__turn]):
            self.__context.can_castle[self.__turn] = (False, self.__context.can_castle[self.__turn][1])
        # king side
        elif self.__context.can_castle[self.__turn][1] and Square(move.fromsq) == Square(
                'h' + self.initialrank[self.__turn]):
            self.__context.can_castle[self.__turn] = (self.__context.can_castle[self.__turn][0], False)
        # en passant
        ep = (move.fromsq + move.tosq) / 2 if move.kind is MoveKind.PAWN2 else None
        self.__context = self.__context._replace(ep=ep)
        self.__turn = self.__turn.opponent()
        if move.kind in (MoveKind.CAPTURE, MoveKind.EP_CAPTURE, MoveKind.PROMOTION_CAPTURE):
            return antimove.addpiece, antimove.addpos
        else:
            return NoPiece(), None

    def unmake(self):
        if len(self.__history) == 0:
            raise RuntimeError('Tried to unmake a move, but no moves had been made previously')
        last = self.__history.pop()
        last.antimove.kind.exec(
            last.antimove, self.__board.movepiece, self.__board.addpiece, self.__board.removepiece)
        self.__context = self.__context._replace(ep=last.ep, can_castle=last.can_castle)
        self.__turn = last.turn

    def getboard(self):
        return self.__board

    def get_moves(self):
        legalmoves = []
        for square in self.__board.get_playersquares(self.turn()):
            legalmoves.append((square, self.moves(square)))
