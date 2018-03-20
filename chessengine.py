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
        return BoardLike(copylist)


class Board(BoardLike):

    def __init__(self, datalist):
        super().__init__(datalist)
        # { [side: Side]: {[key: Square]: bool?} }
        self.__playersquares = {
            Side.WHITE: {},
            Side.BLACK: {}
        }
        for sq, piece in enumerate(self._board):
            if Square(sq) is not None and piece.side is not None:
                self.__playersquares[piece.side][Square(sq)] = True

    def replace(self, square, newcontent):
        return Board(super().replace(square, newcontent)._board)

    def attacked(self, square, side):
        for fromsq in self.__playersquares[side]:
            if self[fromsq].attacks(fromsq, square, self):
                return True
        return False

    def _movepiece(self, fromsq, tosq):
        fromsq = Square(fromsq)
        tosq = Square(tosq)
        piece = self._board[fromsq.index]
        # tabuleiro
        self._board[fromsq.index] = NoPiece()
        self._board[tosq.index] = piece
        # lista de quadrados do jogador
        del self.__playersquares[piece.side][fromsq]
        self.__playersquares[piece.side][tosq] = True

    def _addpiece(self, piece, square):
        square = Square(square)
        # tabuleiro
        self._board[square.index] = piece
        # lista de quadrados do jogador
        self.__playersquares[piece.side][square] = True

    def _removepiece(self, square):
        square = Square(square)
        side = self._board[square.index].side
        # tabuleiro
        self._board[square.index] = NoPiece()
        # lista de quadrados do jogador
        del self.__playersquares[side][square]


Move = namedtuple('Move', 'fromsq tosq kind promotion')


class MoveKind(Enum):
    QUIET = 0
    CAPTURE = 1
    PAWN2 = 2
    EP_CAPTURE = 4
    PROMOTION = 8
    CASTLE_KING = 16
    CASTLE_QUEEN = 32


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
        while isinstance(board[currsq], NoPiece):
            currsq += increment
        if currsq == fromsq:
            return True
        return False

    def plmoves(self, fromsq, board, context):
        moves = []
        for direction in self.directions:
            currindex = 15 * 15 // 2
            while True:
                currindex += direction
                if board[currindex].kind is OutOfBoundsPiece:
                    break
                elif board[currindex].kind is NoPiece:
                    moves.append(Move(fromsq, currindex, MoveKind.QUIET, None))
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
        # Promotion
        if Square(fromsq).rank == self.initialrank[self.side.opponent()] \
                and board[fromsq + self.walkoffset[self.side]].kind is NoPiece:
            for piece in (Rook, Bishop, Knight, Queen):
                moves.append(
                    Move(fromsq, fromsq + self.walkoffset[self.side], MoveKind.PROMOTION, piece))
            canpromote = True
        # En passant capture
        if context.ep is not None and context.ep - fromsq in self.attackoffsets[self.side]:
            moves.append(Move(fromsq, context.ep, MoveKind.EP_CAPTURE, None))
        # Normal move
        if not canpromote and board[fromsq + self.walkoffset[self.side]].kind is NoPiece:
            moves.append(Move(fromsq, fromsq + self.walkoffset[self.side], MoveKind.QUIET, None))
        return moves


class King(Piece):
    offsets = (-1, -16, -15, -14, 1, 16, 15, 14)

    def attacks(self, fromsq, tosq, board):
        return tosq - fromsq in self.offsets

    def plmoves(self, fromsq, board, context):
        moves = []
        # Quiet moves
        for offset in self.offsets:
            if board[fromsq + offset].kind is NoPiece:
                moves.append(Move(fromsq, fromsq + offset, MoveKind.QUIET, None))
        # Castling
