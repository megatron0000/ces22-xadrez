from chessengine import *
from guiengine import *

initialize()

SBD = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png').scale(1 / 10)
SBL = Image('resources/Cburnett V2 improved/PNGs/square brown light_png.png').scale(1 / 10)
SGD = Image('resources/Cburnett V2 improved/PNGs/square gray dark _png.png').scale(1 / 10)
SGL = Image('resources/Cburnett V2 improved/PNGs/square gray light _png.png').scale(1 / 10)
PIECES = {
    Bishop(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_bishop_png_withShadow.png').scale(1 / 10),
    King(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_king_png_withShadow.png').scale(1 / 10),
    Knight(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_knight_png_withShadow.png').scale(1 / 10),
    Pawn(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_pawn_png_withShadow.png').scale(1 / 10),
    Queen(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_queen_png_withShadow.png').scale(1 / 10),
    Rook(Side.BLACK): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/b_rook_png_withShadow.png').scale(1 / 10),
    Bishop(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_bishop_png_withShadow.png').scale(1 / 10),
    King(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_king_png_withShadow.png').scale(1 / 10),
    Knight(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_knight_png_withShadow.png').scale(1 / 10),
    Pawn(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_pawn_png_withShadow.png').scale(1 / 10),
    Queen(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_queen_png_withShadow.png').scale(1 / 10),
    Rook(Side.WHITE): Image(
        'resources/Cburnett V2 improved/PNGs/With Shadow/w_rook_png_withShadow.png').scale(1 / 10)
}


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


class PlayScreen(Scene):
    """
    Classe que monta a tela de jogo.
    """
    pass


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


GameObject(Display(800, 600), MainMenuScreen).gameloop()
