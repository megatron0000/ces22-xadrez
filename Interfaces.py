from chessengine import *
from guiengine import *

WIDTH = 800
HEIGHT = 600
SCALE = 1/15
GAME = None

initialize(WIDTH, HEIGHT)

SBD = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png').scale(SCALE)
SBL = Image('resources/Cburnett V2 improved/PNGs/square brown light_png.png').scale(SCALE)
SGD = Image('resources/Cburnett V2 improved/PNGs/square gray dark _png.png').scale(SCALE)
SGL = Image('resources/Cburnett V2 improved/PNGs/square gray light _png.png').scale(SCALE)
inactive_square = [SBD,SGD]
active_square = [SBL,SGL]


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
    "a1": Rook(Side.WHITE), "b1": Knight(Side.WHITE),"c1":Bishop(Side.WHITE), "d1":Queen(Side.WHITE),
    "e1":King(Side.WHITE), "f1":Bishop(Side.WHITE),"g1":Knight(Side.WHITE), "h1": Rook(Side.WHITE),
    "a2": Pawn(Side.WHITE),"b2": Pawn(Side.WHITE),"c2": Pawn(Side.WHITE),"d2": Pawn(Side.WHITE),
    "e2": Pawn(Side.WHITE),"f2": Pawn(Side.WHITE),"g2": Pawn(Side.WHITE),"h2": Pawn(Side.WHITE),
    "a8": Rook(Side.BLACK), "b8": Knight(Side.BLACK), "c8":Bishop(Side.BLACK), "d8":Queen(Side.BLACK),
    "e8":King(Side.BLACK), "f8":Bishop(Side.BLACK),"g8":Knight(Side.BLACK), "h8": Rook(Side.BLACK),
    "a7": Pawn(Side.BLACK),"b7": Pawn(Side.BLACK),"c7": Pawn(Side.BLACK),"d7": Pawn(Side.BLACK),
    "e7": Pawn(Side.BLACK),"f7": Pawn(Side.BLACK),"g7": Pawn(Side.BLACK),"h7": Pawn(Side.BLACK),
}


class BoardSquare(FigureNode):
    def __init__(self,square,xy):

        self.__square = Square(square)
        super().__init__(xy,inactive_square[self.__square.index%2])


class ChessPiece(FigureNode):
    def __init__(self,piece,xy,square):
        super().__init__(xy,PIECES[piece])
        self.__image = PIECES[piece]
        self.calcpos(xy)
        self.square = square
        self.Mousepiece(self).watch(self._bus, lambda: self.bounds)


    def calcpos(self,xy):
        x = xy[0] + (SBD.width - self.__image.width) / 2
        y = xy[1] + (SBD.height - self.__image.height) / 2
        self.xy((x,y))

    class Mousepiece (MouseAware):
        def __init__(self,outer):
            super().__init__()
            self.outer = outer
        def onclick(self):
            print(GAME.moves(self.outer.square))




class MainMenuScreen(Scene):
    """
    Classe que monta o menu principal.
    """

    def _parts(self):
        play_button = ButtonNode((300, 200), Text("Jogar", 36, None, (255, 255, 255), (139, 69, 19)))
        tutorial_button = ButtonNode((300, 400), Text("Tutorial", 36, None, (255, 255, 255), (139, 69, 19)))
        self._background((184, 134, 11))
        self._add_child(play_button)
        self._add_child(tutorial_button)
        play_button.onclick(self.clickplay)

    def clickplay (self):
        self._bus.emit(Event.SCENE_CHANGE,PlayScreen)


class PlayScreen(Scene):
    """
    Classe que monta a tela de jogo.
    """
    def _parts(self):
        listagame = []
        margemx = (WIDTH- 8*SBD.width)/2
        margemy = (HEIGHT - 8 * SBD.height)/ 2
        xplus = 0
        posicoes = []
        for c in "abcdefgh":
            for i in range(1,9):
                self._add_child(BoardSquare(c+str(i),(margemx + xplus, margemy + (8-i)*SBD.height)))
                posicoes.append((c+str(i),(margemx + xplus, margemy + (8-i)*SBD.height)))
            xplus += SBD.width

        for posic in posicoes:
            if PIECES_INIT.get(posic[0]) is not None:
                self._add_child(ChessPiece(PIECES_INIT.get(posic[0]),posic[1],Square(posic[0])))

        for i in range(8):
            for j in range(8):
                peca = PIECES_INIT.get(posicoes[i+8*j][0])
                if peca is None:
                    listagame.append(NoPiece())
                else:
                    listagame.append(peca)

        global GAME
        GAME = Game(listagame,{Side.WHITE:(False,False),Side.BLACK:(False,False)},None,Side.WHITE)




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
