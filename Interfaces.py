from chessengine import *
from guiengine import *

WIDTH = 800
HEIGHT = 600
SCALE = 1 / 15
GAME = None

initialize(WIDTH, HEIGHT)

SBD = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png').scale(SCALE)
SBL = Image('resources/Cburnett V2 improved/PNGs/square brown light_png.png').scale(SCALE)
SGD = Image('resources/Cburnett V2 improved/PNGs/square gray dark _png.png').scale(SCALE)
SGL = Image('resources/Cburnett V2 improved/PNGs/square gray light _png.png').scale(SCALE)
INACTIVE_SQUARE = [SBD, SGD]
ACTIVE_SQUARE = [SBL, SGL]

PIECES = {
    Bishop(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_bishop_png_withShadow.png').scale(SCALE),
    King(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_king_png_withShadow.png').scale(SCALE),
    Knight(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_knight_png_withShadow.png').scale(SCALE),
    Pawn(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_pawn_png_withShadow.png').scale(SCALE),
    Queen(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_queen_png_withShadow.png').scale(SCALE),
    Rook(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_rook_png_withShadow.png').scale(SCALE),
    Bishop(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_bishop_png_withShadow.png').scale(SCALE),
    King(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_king_png_withShadow.png').scale(SCALE),
    Knight(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_knight_png_withShadow.png').scale(SCALE),
    Pawn(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_pawn_png_withShadow.png').scale(SCALE),
    Queen(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_queen_png_withShadow.png').scale(SCALE),
    Rook(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_rook_png_withShadow.png').scale(SCALE)
}

PIECES_INIT = {
    "a1": Rook(Side.WHITE), "b1": Knight(Side.WHITE), "c1": Bishop(Side.WHITE),
    "d1": Queen(Side.WHITE), "e1": King(Side.WHITE), "f1": Bishop(Side.WHITE),
    "g1": Knight(Side.WHITE), "h1": Rook(Side.WHITE), "a2": Pawn(Side.WHITE),
    "b2": Pawn(Side.WHITE), "c2": Pawn(Side.WHITE), "d2": Pawn(Side.WHITE),
    "e2": Pawn(Side.WHITE), "f2": Pawn(Side.WHITE), "g2": Pawn(Side.WHITE),
    "h2": Pawn(Side.WHITE), "a8": Rook(Side.BLACK), "b8": Knight(Side.BLACK),
    "c8": Bishop(Side.BLACK), "d8": Queen(Side.BLACK), "e8": King(Side.BLACK),
    "f8": Bishop(Side.BLACK), "g8": Knight(Side.BLACK), "h8": Rook(Side.BLACK),
    "a7": Pawn(Side.BLACK), "b7": Pawn(Side.BLACK), "c7": Pawn(Side.BLACK),
    "d7": Pawn(Side.BLACK), "e7": Pawn(Side.BLACK), "f7": Pawn(Side.BLACK),
    "g7": Pawn(Side.BLACK), "h7": Pawn(Side.BLACK),
}


class BoardSquare(FigureNode):
    class BoardMouse(MouseAware):
        def __init__(self, outer):
            super().__init__()
            self.outer = outer

        def onclick(self):
            self.outer._bus.emit('moves markup', [])

    def __init__(self, square, xy):
        self.__square = Square(square)
        super().__init__(xy, INACTIVE_SQUARE[self.__square.index % 2])
        self.BoardMouse(self).watch(self._bus, lambda: self.bounds)
        self._bus.on('moves markup', self.markup)
        self._bus.on('request square change', self.respond_squarechange)

    def markup(self, moves):
        if self.__square in [move.tosq for move in moves]:
            self.set_image(ACTIVE_SQUARE[self.__square.index % 2])
        else:
            self.set_image(INACTIVE_SQUARE[self.__square.index % 2])

    def respond_squarechange(self, pos_self_fromsq):
        if not self.bounds.collidepoint(pos_self_fromsq[0]):
            return
        # print(str(self.__square.name + " responds to" + str(pos_self_fromsq[0])))
        # print(pos_self_fromsq[2], GAME.get(pos_self_fromsq[2]))
        move = next((x for x in GAME.moves(pos_self_fromsq[2]) if
                     x.fromsq == pos_self_fromsq[2] and x.tosq == self.__square), None)
        if move is not None:
            self._bus.emit(
                'respond square change', (self.bounds.topleft, pos_self_fromsq[1], move))


class ChessPiece(FigureNode):
    def __init__(self, piece, xy, square):
        super().__init__(xy, PIECES[piece])
        self.image = PIECES[piece]
        self.calcpos(xy)
        self.piece = piece
        self.square = square
        self.Mousepiece(self).watch(self._bus, lambda: self.bounds)

    def calcpos(self, xy):
        x = xy[0] + (SBD.width - self.image.width) / 2
        y = xy[1] + (SBD.height - self.image.height) / 2
        self.xy((x, y))

    class Mousepiece(MouseAware):
        def __init__(self, outer):
            super().__init__()
            self.outer = outer
            self.outer._bus.on('respond square change', self.on_response_squarechange)
            self.draglastpos = None
            self.originalpos = None

        def on_response_squarechange(self, pos_self_move):
            if self is not pos_self_move[1]:
                return
            self.outer.calcpos(pos_self_move[0])
            self.outer.square = pos_self_move[2].tosq
            captured = GAME.make(pos_self_move[2])
            if captured.kind is not NoPiece:
                self.outer._bus.emit('piece captured', (captured, pos_self_move[2].tosq))

        def onclick(self):
            self.outer._bus.emit('moves markup', GAME.moves(self.outer.square))

        def ondragstart(self, pos):
            self.draglastpos = pos
            self.originalpos = self.outer.xy()

        def ondrag(self, pos):
            newxy = tuple(
                orig + x1 - x0 for orig, x1, x0 in zip(self.outer.xy(), pos, self.draglastpos))
            self.outer.xy(newxy)
            self.draglastpos = pos

        def ondragend(self, pos):
            self.outer.xy(self.originalpos)
            self.outer._bus.emit('request square change', (pos, self, self.outer.square))


class MainMenuScreen(Scene):
    """
    Classe que monta o menu principal.
    """

    def _parts(self):
        play_button = ButtonNode(
            (300, 200), Text("Jogar", 36, None, (255, 255, 255), (139, 69, 19)))
        tutorial_button = ButtonNode(
            (300, 400), Text("Tutorial", 36, None, (255, 255, 255), (139, 69, 19)))
        self._background((184, 134, 11))
        self._add_child(play_button)
        self._add_child(tutorial_button)
        play_button.onclick(self.clickplay)
        # self._bgm(Sound('Music/Music.ogg'))

    def clickplay(self):
        self._bus.emit(Event.SCENE_CHANGE, PlayScreen)


class PlayScreen(Scene):
    """
    Classe que monta a tela de jogo.
    """

    children = []

    def on_piececaptured(self, piece_square):
        child = next(chesspiece for chesspiece in self.children if
                     chesspiece.piece == piece_square[0] and chesspiece.square == piece_square[1])
        self._remove_child(child)
        self.children.remove(child)

    def _parts(self):
        listagame = []
        margemx = (WIDTH - 8 * SBD.width) / 2
        margemy = (HEIGHT - 8 * SBD.height) / 2
        xplus = 0
        posicoes = []
        for c in "abcdefgh":
            for i in range(1, 9):
                self._add_child(
                    BoardSquare(c + str(9 - i), (margemx + xplus, margemy + (i - 1) * SBD.height)))
                posicoes.append((c + str(9 - i), (margemx + xplus, margemy + (i - 1) * SBD.height)))
            xplus += SBD.width

        for posic in posicoes:
            if PIECES_INIT.get(posic[0]) is not None:
                newchild = ChessPiece(PIECES_INIT.get(posic[0]), posic[1], Square(posic[0]))
                self.children.append(newchild)
                self._add_child(newchild)

        for i in range(8):
            for j in range(8):
                peca = PIECES_INIT.get(posicoes[i + 8 * j][0])
                if peca is None:
                    listagame.append(NoPiece())
                else:
                    listagame.append(peca)

        global GAME
        GAME = Game(
            listagame, {Side.WHITE: (False, False), Side.BLACK: (False, False)}, None, Side.WHITE)

        self._bus.on('piece captured', self.on_piececaptured)


class TutorialScreen(Scene):
    """
    Classe que monta a tela de tutorial.
    """

    """PawnMovesButton =
    RookMovesButton =
    KnightMovesButton =
    BishopMovesButton =
    QueenMovesButton =
    KingMovesButton =
    """
    pass


GameObject(Display(WIDTH, HEIGHT), MainMenuScreen).gameloop()
