from guiengine import *

pygame.init()
pygame.display.set_mode((800, 600))

sbd = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png').scale(1 / 10)
sbl = Image('resources/Cburnett V2 improved/PNGs/square brown light_png.png').scale(1 / 10)
sgd = Image('resources/Cburnett V2 improved/PNGs/square gray dark _png.png').scale(1 / 10)
sgl = Image('resources/Cburnett V2 improved/PNGs/square gray light _png.png').scale(1 / 10)
music = Sound('Music/Music.ogg')


class BrownSquare(FigureNode):
    class MouseAware(MouseAware):

        def __init__(self, outer):
            super().__init__(lambda: outer.bounds)
            self.outer = outer
            self.mouse_pos_old = None

        def onmouseenter(self):
            self.outer.set_image(sbl)

        def onmouseleave(self):
            self.outer.set_image(sbd)

        def ondragstart(self, pos):
            self.mouse_pos_old = pos
            self.outer._bus.emit('estou sendo arrastado', None)

        def ondrag(self, data):
            self.outer.xy(tuple(l0 + l1 - l2 for l0, l1, l2 in
                                zip(self.outer.xy(), data, self.mouse_pos_old)))
            self.mouse_pos_old = data

        def ondragend(self, data):
            self.mouse_pos_old = None

        def onclick(self):
            self.outer._bus.emit(Event.SCENE_CHANGE, EndScene)

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> implementando-chessengine
=======
>>>>>>> 8a57
    def __init__(self, xy):
        super().__init__(xy, sbd)
        self.MouseAware(self).watch(self._bus)


class MyText(TextNode):

    def __init__(self):
        self.text = Text('Tente arrastar um quadrado !', 28, None, (255, 255, 0))
        super().__init__((100, 400), self.text)
        self._bus.on('estou sendo arrastado', self.change)

    def change(self, data):
        self.text.content('Perfeito ! Arrastou, funcionou. Agora tente clicar num quadrado')


class MyScene(Scene):

    def _parts(self):
        self._bgm(music)
        for i in range(8):
<<<<<<< HEAD
<<<<<<< HEAD
            self._add_child(BrownSquare((i * (sbd.width + 10), 50)))
        self._add_child(MyText())

=======
            self._add_child(BrownSquare((i * (sbd.width + 1), 50)))
        self._add_child(MyText())


>>>>>>> implementando-chessengine
=======
            self._add_child(BrownSquare((i * (sbd.width + 1), 50)))
        self._add_child(MyText())


>>>>>>> 8a57
class EndScene(Scene):

    def _parts(self):
        self._add_child(TextNode((10, 300),
                                 Text('Você vem para esta tela quando clica num quadrado',
                                      40, None, (255, 0, 255))))


GameObject(Display(800, 600), MyScene).gameloop()
