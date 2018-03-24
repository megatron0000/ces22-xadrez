from guiengine import *
import pygame

class MainMenuScreen(Scene):
    """
    Classe que monta o menu principal.
    """

    def _parts(self):
        PlayButton = ButtonNode((300, 200), Text("Jogar", 36, None, (255, 255, 255), (139,69,19)))
        TutorialButton = ButtonNode((300, 400), Text("Tutorial", 36, None, (255, 255, 255), (139,69,19)))
        self._background((184, 134, 11))
        self._add_child(PlayButton)
        self._add_child(TutorialButton)


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


pygame.init()
pygame.display.set_mode((800, 600))

GameObject(Display(800, 600), MainMenuScreen).gameloop()
