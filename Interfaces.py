from guiengine import *
import pygame

class TutorialButtonNode(ButtonNode):
    class MouseAware(MouseAware):

        def __init__(self, outer):
            super().__init__(lambda: outer.bounds)
            self.outer = outer
            self.mouse_pos_old = None

        def onclick(self):
            self.outer._bus.emit(Event.SCENE_CHANGE, TutorialScreen)

class MainMenuScreen(Scene):
    """
    Classe que monta o menu principal.
    """

    def _parts(self):
        Title = TextNode((300, 100), Text('Chess', 100, None, (255, 255, 255), (139, 69, 19)))
        PlayButton = ButtonNode((370, 200), Text("Jogar", 36, None, (255, 255, 255), (139, 69, 19)))
        TutorialButton = TutorialButtonNode((370, 250), Text("Tutorial", 36, None, (255, 255, 255), (139, 69, 19)))
        self._background((184, 134, 11))
        self._add_child(Title)
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

    def _parts(self):
        TutorialTitle = TextNode((150, 100), Text("Tutorial de Movimentos", 70, None, (255, 255, 255), (139, 69, 19)))
        PawnMovesButton = ButtonNode((370, 200), Text("Peão", 36, None, (255, 255, 255), (139, 69, 19)))
        RookMovesButton = ButtonNode((370, 250), Text("Torre", 36, None, (255, 255, 255), (139, 69, 19)))
        KnightMovesButton = ButtonNode((370, 300), Text("Cavalo", 36, None, (255, 255, 255), (139, 69, 19)))
        BishopMovesButton = ButtonNode((370, 350), Text("Bispo", 36, None, (255, 255, 255), (139, 69, 19)))
        QueenMovesButton = ButtonNode((370, 400), Text("Rainha", 36, None, (255, 255, 255), (139, 69, 19)))
        KingMovesButton = ButtonNode((370, 450), Text("Rei", 36, None, (255, 255, 255), (139, 69, 19)))

        self._background((184, 134, 11))
        self._add_child(TutorialTitle)
        self._add_child(PawnMovesButton)
        self._add_child(RookMovesButton)
        self._add_child(KnightMovesButton)
        self._add_child(BishopMovesButton)
        self._add_child(QueenMovesButton)
        self._add_child(KingMovesButton)


pygame.init()
pygame.display.set_mode((800, 600))

GameObject(Display(800, 600), MainMenuScreen).gameloop()
