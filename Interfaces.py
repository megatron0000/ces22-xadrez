from math import sqrt

from chessengine import *
from guiengine import *

WIDTH = 800
HEIGHT = 600
SCALE = 1 / 15
GAME = None
CHOOSINGPROMOTION = False

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

    def __init__(self, square, xy):
        self.square = Square(square)
        super().__init__(xy, INACTIVE_SQUARE[self.square.index % 2])
        self.BoardMouse(self).watch(self._bus, lambda: self.bounds)
        self._bus.on('moves markup', self.markup)
        self._bus.on('request square change', self.respond_squarechange)

    def markup(self, moves):
        if self.square in [move.tosq for move in moves]:
            self.set_image(ACTIVE_SQUARE[self.square.index % 2])
        else:
            self.set_image(INACTIVE_SQUARE[self.square.index % 2])

    def respond_squarechange(self, pos_self_fromsq):
        if not self.bounds.collidepoint(pos_self_fromsq[0]):
            return
        move = next((x for x in GAME.moves(pos_self_fromsq[2]) if
                     x.fromsq == pos_self_fromsq[2] and x.tosq == self.square), None)
        if move is not None:
            self._bus.emit(
                'respond square change', (self.bounds.topleft, pos_self_fromsq[1], move))

    class BoardMouse(MouseAware):
        def __init__(self, outer):
            """

            :type outer ChessPiece
            """
            super().__init__()
            self.outer = outer

        def onclick(self):
            self.outer._bus.emit('moves markup', [])


class ChessPiece(FigureNode):
    def __init__(self, piece, xy, square):
        super().__init__(xy, PIECES[piece])
        self.image = PIECES[piece]
        self.calcpos(xy)
        self.piece = piece
        self.square = square
        self.PieceAware(self).watch(self._bus, lambda: self.bounds)
        self.ismoving = False
        self.movedirection = (0, 0)
        self.movetarget = (0, 0)
        self.timetaken = 0

    def calcpos(self, xy):
        x = xy[0] + (SBD.width - self.image.width) / 2
        y = xy[1] + (SBD.height - self.image.height) / 2
        self.xy((x, y))

    def update_logic(self, dt):
        super().update_logic(dt)
        if self.timetaken > 0:
            self.xy(tuple(l1 + 1000 * dt * l2 for l1, l2 in zip(self.xy(), self.movedirection)))
            self.timetaken -= dt
            if self.timetaken <= 0:
                self.calcpos(self.movetarget)

    class PieceAware(MouseAware):
        def __init__(self, outer):
            """

            :type outer ChessPiece
            """
            super().__init__()
            self.outer = outer
            self.outer._bus.on('respond square change', self.on_response_squarechange)
            self.outer._bus.on('order piece move', self.on_order_piece_move)
            self.draglastpos = None
            self.originalpos = None

        def on_response_squarechange(self, pos_self_move):
            if self is not pos_self_move[1]:
                return
            self.outer.calcpos(pos_self_move[0])
            self.outer.square = pos_self_move[2].tosq
            if pos_self_move[2].promotion is not None:
                self.outer._bus.emit('request promotion options', (self.outer, pos_self_move[2]))
                captured = GAME.get(pos_self_move[2].tosq)
                if captured.kind is not NoPiece:
                    self.outer._bus.emit('piece captured', (captured, pos_self_move[2].tosq))
                global CHOOSINGPROMOTION
                CHOOSINGPROMOTION = True
                return
            captured = GAME.make(pos_self_move[2])
            self.outer._bus.emit('move made', None)
            if captured[0].kind is not NoPiece:
                self.outer._bus.emit('piece captured', captured)
            if pos_self_move[2].kind is MoveKind.CASTLE_QUEEN:
                self.outer._bus.emit('request piece move', (self.outer.square - 2, self.outer.square + 1))
            elif pos_self_move[2].kind is MoveKind.CASTLE_KING:
                self.outer._bus.emit('request piece move', (self.outer.square + 1, self.outer.square - 1))

        def on_order_piece_move(self, self_tosq_coord):
            if self.outer is not self_tosq_coord[0]:
                return
            self.outer.square = self_tosq_coord[1]
            self.outer.ismoving = True
            self.outer.movedirection = tuple(
                l2 - l1 for l1, l2 in zip(self.outer.xy(), self_tosq_coord[2]))
            length = sqrt(self.outer.movedirection[0] * self.outer.movedirection[0]
                          + self.outer.movedirection[1] * self.outer.movedirection[1])
            self.outer.movedirection = tuple(l / length for l in self.outer.movedirection)
            self.outer.movetarget = self_tosq_coord[2]
            self.outer.timetaken = length / 1000

        def ondragstart(self, pos):
            if self.outer.ismoving:
                return
            self.outer._bus.emit('moves markup', GAME.moves(self.outer.square))
            self.draglastpos = pos
            self.originalpos = self.outer.xy()

        def ondrag(self, pos):
            if self.outer.ismoving:
                return
            newxy = tuple(
                orig + x1 - x0 for orig, x1, x0 in zip(self.outer.xy(), pos, self.draglastpos))
            self.outer.xy(newxy)
            self.draglastpos = pos

        def ondragend(self, pos):
            if self.outer.ismoving:
                return
            self.outer._bus.emit('moves markup', [])
            self.outer.xy(self.originalpos)
            if not CHOOSINGPROMOTION:
                self.outer._bus.emit('request square change', (pos, self, self.outer.square))


class PromotionOption(FigureNode):
    class PromotionOptionMouseAware(MouseAware):

        def __init__(self, outer):
            super().__init__()
            self.outer = outer

        def onmouseenter(self):
            self.outer.set_image(
                PIECES[self.outer.chesspiece].clone(apply_changes=False).scale(SCALE * 1.2))

        def onmouseleave(self):
            self.outer.set_image(PIECES[self.outer.chesspiece].clone())

        def onclick(self):
            self.outer._bus.emit('promotion choosen', self.outer.chesspiece)

    def __init__(self, xy, chesspiece):
        self.chesspiece = chesspiece
        super().__init__(xy, PIECES[self.chesspiece].clone())
        self.PromotionOptionMouseAware(self).watch(self._bus, lambda: self.bounds)


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
    promoting_uipiece = None
    promoting_move = None
    special_condition_message = None
    special_condition_button = None

    def on_piececaptured(self, piece_square):
        child = next(chesspiece for chesspiece in self.children if
                     isinstance(chesspiece, ChessPiece)
                     and chesspiece.piece == piece_square[0] and chesspiece.square == piece_square[1])
        self._remove_child(child)
        self.children.remove(child)

    def on_request_piece_move(self, fromsq_tosq):
        child = next(piece for piece in self.children if piece.square == fromsq_tosq[0]
                     and isinstance(piece, ChessPiece))
        square = next(sq for sq in self.children if sq.square == fromsq_tosq[1]
                      and isinstance(sq, BoardSquare))
        self._bus.emit('order piece move', (child, fromsq_tosq[1], square.xy()))

    def on_request_promotion_options(self, uipiece_move):
        self.promoting_uipiece = uipiece_move[0]
        self.promoting_move = uipiece_move[1]
        side = uipiece_move[0].piece.side
        choose_text = Text('Escolha uma promoção', 40, None, (255, 255, 255), (0, 0, 0))
        marginx = (WIDTH - 8 * SBD.width) / 2
        marginy = (HEIGHT - 8 * SBD.height) / 2
        posx = (WIDTH - choose_text.width()) / 2
        posy = ((HEIGHT - 8 * SBD.height) / 2 - choose_text.height()) / 2
        choose_button = TextNode((posx, posy), choose_text)
        self.children.append(choose_button)
        self._add_child(choose_button)
        deltay = 0
        for piece in [Rook(side), Queen(side), Bishop(side), Knight(side)]:
            image = PIECES[piece]
            option = PromotionOption(
                (marginx + 8 * SBD.width + (marginx - image.width) / 2,
                 deltay + marginy),
                piece)
            self._add_child(option)
            self.children.append(option)
            deltay += 2 * image.height

    def on_promotion_choosen(self, chesspiece):
        xy = next(square.xy() for square in self.children if isinstance(square, BoardSquare) and
                  square.square == self.promoting_uipiece.square)
        square = self.promoting_uipiece.square
        promotedpiece = ChessPiece(chesspiece, xy, square)
        for element in self.children[-5:]:
            self._remove_child(element)
            self.children.remove(element)
        self.children.remove(self.promoting_uipiece)
        self._remove_child(self.promoting_uipiece)
        self._add_child(promotedpiece)
        self.children.append(promotedpiece)
        global CHOOSINGPROMOTION
        CHOOSINGPROMOTION = False
        GAME.make(self.promoting_move._replace(promotion=chesspiece))
        self._bus.emit('move made', None)

    def on_move_made(self, data):

        def change_message(text, color):
            marginy = (HEIGHT - 8 * SBD.height) / 2
            self.special_condition_message.content(text)
            self.special_condition_message.color(color)
            self.special_condition_button.xy((
                (WIDTH - self.special_condition_message.width()) / 2,
                marginy + 8 * SBD.height + (marginy - self.special_condition_message.height()) / 2
            ))

        if GAME.stalemate():
            change_message(
                'EMPATE ! Não há movimentos possíveis. Retorne ao menu principal', (123, 70, 203))
        elif GAME.checkmate():
            change_message('XEQUE-MATE ! Retorne ao menu principal', (242, 68, 43))
        elif GAME.check():
            change_message('XEQUE !', (255, 165, 0))
        else:
            change_message('', (0, 0, 0))

    def _parts(self):
        self.children = []
        self.promoting_uipiece = None
        self.promoting_move = None
        listagame = []
        margemx = (WIDTH - 8 * SBD.width) / 2
        margemy = (HEIGHT - 8 * SBD.height) / 2
        self.special_condition_message = Text('', 40, None, (255, 255, 255), (0, 0, 0))
        self.special_condition_button = TextNode((0, 0), self.special_condition_message)
        self._add_child(self.special_condition_button)
        back_text = Text('Menu', 40, None, (0, 0, 0), (173, 216, 230))
        back_button = ButtonNode(
            ((margemx - back_text.width()) / 2,
             (HEIGHT - back_text.height()) / 2),
            back_text)
        back_button.onclick(lambda: self._bus.emit(Event.SCENE_CHANGE, MainMenuScreen))
        self._add_child(back_button)
        xplus = 0
        posicoes = []
        for c in "abcdefgh":
            for i in range(1, 9):
                newchild = BoardSquare(c + str(9 - i), (margemx + xplus, margemy + (i - 1) * SBD.height))
                self.children.append(newchild)
                self._add_child(newchild)
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
            listagame, {Side.WHITE: (True, True), Side.BLACK: (True, True)}, None, Side.WHITE)

        self._bus.on('piece captured', self.on_piececaptured)
        self._bus.on('request piece move', self.on_request_piece_move)
        self._bus.on('request promotion options', self.on_request_promotion_options)
        self._bus.on('promotion choosen', self.on_promotion_choosen)
        self._bus.on('move made', self.on_move_made)


GameObject(Display(WIDTH, HEIGHT), MainMenuScreen).gameloop()
