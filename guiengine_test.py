import unittest

from guiengine import *


def initpygame():
    pygame.init()
    pygame.display.set_mode((800, 600))


class TestEventBus(unittest.TestCase):

    def gen_cb(self, number):
        def cb(data):
            if data == 1:
                self.called[number] = True

        return cb

    def setUp(self):
        self.bus = EventBus()
        self.called = {}

    def tearDown(self):
        EventBus.active(None)

    def test_emission(self):
        self.bus.on('event_1', self.gen_cb(1))
        self.bus.on('event_1', self.gen_cb(2))
        self.bus.on('event_2', self.gen_cb(3))
        self.bus.emit('event_1', 1)
        self.bus.emit('event_2', 1)
        self.assertEqual(self.called.get(1), True)
        self.assertEqual(self.called.get(2), True)
        self.assertEqual(self.called.get(3), True)

    def test_disable(self):
        cb1 = self.gen_cb(1)
        cb2 = self.gen_cb(2)
        cb3 = self.gen_cb(3)
        self.bus.on('event_1', cb1)
        self.bus.on('event_1', cb2)
        self.bus.on('event_1', cb3)
        self.bus.disable('event_1', cb2)
        self.bus.emit('event_1', 1)
        self.assertEqual(self.called.get(1), True)
        self.assertEqual(self.called.get(2), None)
        self.assertEqual(self.called.get(3), True)
        self.called = {}
        self.bus.disable('event_1')
        self.bus.emit('event_1', 1)
        self.assertEqual(self.called.get(1), None)
        self.assertEqual(self.called.get(2), None)
        self.assertEqual(self.called.get(3), None)

    def test_disable_all(self):
        self.bus.on('event_1', self.gen_cb(1))
        self.bus.on('event_1', self.gen_cb(2))
        self.bus.on('event_2', self.gen_cb(3))
        self.bus.disable_all()
        self.bus.emit('event_1', 1)
        self.bus.emit('event_2', 1)
        self.assertEqual(self.called.get(1), None)
        self.assertEqual(self.called.get(2), None)
        self.assertEqual(self.called.get(2), None)

    def test_active(self):
        inst = EventBus()
        # EventBus.active(None)
        # self.assertIsNone(EventBus.active())
        EventBus.active(inst)
        self.assertEqual(EventBus.active(), inst)


class TestBusProxy(unittest.TestCase):

    def setUp(self):
        self.bus = EventBus()
        EventBus.active(self.bus)
        self.proxy = BusProxy()
        self.called = {}

    def gen_cb(self, number):
        def cb(data):
            if data == 1:
                self.called[number] = True

        return cb

    def test_emission(self):
        self.bus.on('event_1', self.gen_cb(1))
        self.proxy.on('event_1', self.gen_cb(2))
        self.proxy.emit('event_1', 1)
        self.assertTrue(self.called.get(1))
        self.assertTrue(self.called.get(2))

    def test_disable(self):
        cb0 = self.gen_cb(1)
        cb1 = self.gen_cb(2)
        cb2 = self.gen_cb(3)
        cb3 = self.gen_cb(4)
        self.proxy.on('event_1', cb0)
        self.proxy.on('event_1', cb3)
        self.proxy.on('event_2', cb1)
        self.bus.on('event_1', cb2)
        self.proxy.disable('event_1', cb0)
        self.proxy.emit('event_1', 1)
        self.proxy.emit('event_2', 1)
        self.assertIsNone(self.called.get(1))
        self.assertTrue(self.called.get(2))
        self.assertTrue(self.called.get(3))
        self.assertTrue(self.called.get(4))


class TestOuterBus(unittest.TestCase):
    class Listeners:

        def __init__(self, outer):
            """

            :type outer TestOuterBus
            """
            self.outer = outer
            self.moved = False
            self.button_down = False
            self.button_up = False

        def onmousemove(self, data):
            self.moved = True
            self.outer.assertEqual(data, (50, 50))

        def onbuttondown(self, data):
            self.button_down = True
            self.outer.assertEqual(data, (40, 60))

        def onbuttonup(self, data):
            self.button_up = True
            self.outer.assertEqual(data, (40, 60))

    def setUp(self):
        self.outer_bus = OuterBus()
        self.mousemove = pygame.event.Event(pygame.MOUSEMOTION, {
            'pos': (50, 50),
            'rel': (-10, 30),
            'buttons': (False, False, False)
        })
        self.buttondown = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            'button': 1,
            'pos': (40, 60)
        })
        self.buttonup = pygame.event.Event(pygame.MOUSEBUTTONUP, {
            'button': 1,
            'pos': (40, 60)
        })
        self.listeners = self.Listeners(self)

    def _launch(self, listen_on_bus):
        pygame.event.post(self.mousemove)
        pygame.event.post(self.buttondown)
        pygame.event.post(self.buttonup)
        listen_on_bus.on(Event.MOUSEMOVE, self.listeners.onmousemove)
        listen_on_bus.on(Event.MOUSEUP, self.listeners.onbuttonup)
        listen_on_bus.on(Event.MOUSEDOWN, self.listeners.onbuttondown)

    def test_emit_refresh(self):
        self._launch(self.outer_bus)
        self.outer_bus.refresh()
        self.assertTrue(self.listeners.moved)
        self.assertTrue(self.listeners.button_up)
        self.assertTrue(self.listeners.button_down)

    def test_redirect(self):
        bus = EventBus()
        self.outer_bus.redirect(bus)
        self._launch(bus)
        self.outer_bus.refresh()
        self.assertTrue(self.listeners.moved)
        self.assertTrue(self.listeners.button_up)
        self.assertTrue(self.listeners.button_down)


class TestMouseAware(unittest.TestCase):
    """
    TODO: Testar MouseAware... ou não...
    """

    def test_nothing(self):
        pass


class TestResourceBank(unittest.TestCase):

    def setUp(self):
        initpygame()
        self.bank = ResourceBank.instance()
        self.paths = ['resources/Cburnett V2 improved/PNGs/square brown dark_png.png',
                      'resources/Cburnett V2 improved/PNGs/square brown light_png.png']

    def test_instance(self):
        self.assertEqual(self.bank, ResourceBank.instance())

    def test_image(self):
        self.assertIsInstance(self.bank.image(self.paths[0]), pygame.Surface)

    def test_sound(self):
        sound = self.bank.sound('Music/Music.ogg')
        self.assertIsInstance(sound, pygame.mixer.Sound)

    def test_font(self):
        font = self.bank.font(None, 12)
        self.assertIsInstance(font, pygame.font.Font)

    def test_caching(self):
        self.assertEqual(self.bank.image(self.paths[0]), self.bank.image(self.paths[0]))
        self.assertNotEqual(self.bank.image(self.paths[1]),
                            self.bank.image(self.paths[1], cached=False))


class TestImage(unittest.TestCase):

    def setUp(self):
        initpygame()
        self.image = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png')

    def test_scale(self):
        old_w = self.image.width
        old_h = self.image.height
        new_rf = self.image.scale(2)
        self.assertEqual(self.image.width, old_w * 2)
        self.assertEqual(self.image.height, old_h * 2)
        self.assertEqual(new_rf, self.image)


class TestText(unittest.TestCase):

    def setUp(self):
        self.c1 = 'Hola'
        self.c2 = 'Adios'
        self.txt = Text(self.c1, 12, None, (0, 0, 0), (255, 255, 255))

    def test_to_surface(self):
        # Deve retornar a mesma várias vezes, a não ser quando conteúdo ou cor mudar
        s1 = self.txt.to_surface()
        s2 = self.txt.to_surface()
        self.txt.content(self.c2)
        s3 = self.txt.to_surface()
        s4 = self.txt.to_surface()
        self.txt.color((0, 0, 255))
        s5 = self.txt.to_surface()
        s6 = self.txt.to_surface()
        self.assertIs(s1, s2)
        self.assertIsNot(s1, s3)
        self.assertIs(s3, s4)
        self.assertIsNot(s3, s5)
        self.assertIs(s5, s6)


class TestRootDrawContext(unittest.TestCase):

    def setUp(self):
        self.ctx = RootDrawContext(Surface((500, 500)))
        self.img = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png') \
            .scale(1 / 10)

    def test_blit(self):
        rect = self.ctx.blit(self.img, (30, 30))
        self.assertEqual(rect.x, 30)
        self.assertEqual(rect.y, 30)


class TestDrawContext(unittest.TestCase):

    def setUp(self):
        initpygame()
        self.root = RootDrawContext(Surface((500, 500)))
        self.img = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png') \
            .scale(1 / 10)

    def test_sub_blit(self):
        sub = self.root.sub((40, 40)).sub((60, 60))
        rect = sub.blit(self.img, (50, 50))
        self.assertEqual(rect.x, 40 + 60 + 50)
        self.assertEqual(rect.y, 40 + 60 + 50)


class TestSound(unittest.TestCase):

    def setUp(self):
        self.sound = Sound('Music/Music.ogg')

    def test_not_throws(self):
        self.sound.play(-1).stop().play(0).play(0).play(3).stop()


class TestEmptySound(unittest.TestCase):

    def test_nothing(self):
        EmptySound().play(-1).play(0).stop().play(2).play(3).stop()


class TestRenderizable(unittest.TestCase):

    def setUp(self):
        self.ren = Renderizable((10, 20))

    def test_bounds(self):
        self.assertEqual(self.ren.bounds.x, 10)
        self.assertEqual(self.ren.bounds.y, 20)
        self.assertEqual(self.ren.bounds.width, 0)
        self.assertEqual(self.ren.bounds.height, 0)

    def test_bus(self):
        self.assertIsInstance(self.ren._bus, BusProxy)


class TestFigureNode(unittest.TestCase):
    class MockDrawContext(DrawContext):

        def __init__(self):
            self.blitted = False

        def blit(self, imagelike, xy):
            if xy == (10, 20):
                self.blitted = True

    def setUp(self):
        self.fig = FigureNode((10, 20), Image(
            'resources/Cburnett V2 improved/PNGs/square brown dark_png.png'
        ).scale(1 / 10))

    def test_update_render(self):
        mock = self.MockDrawContext()
        self.fig.update_render(mock, 0.01)
        self.assertTrue(mock.blitted)


class TestLayer(unittest.TestCase):
    class MockNode(Renderizable):

        def __init__(self, bounds):
            super().__init__(bounds.topleft)
            self.logic = False
            self.render = False
            self.destroyed = False
            self.bounds = bounds

        def update_logic(self, dt):
            self.logic = True

        def update_render(self, draw_context: DrawContext, dt):
            self.render = True

        def destroy(self):
            self.destroyed = True

    def setUp(self):
        self.layer = Layer((10, 10))
        self.c1 = TestLayer.MockNode(Rect((10, 10), (30, 40)))
        self.c2 = TestLayer.MockNode(Rect((20, 10), (30, 40)))
        self.layer._add_child(self.c1)
        self.layer._add_child(self.c2)

    def test_update_logic(self):
        self.layer.update_logic(0.01)
        self.assertTrue(self.c1.logic)
        self.assertTrue(self.c2.logic)

    def test_update_render(self):
        self.layer.update_render(RootDrawContext(Surface((10, 10))), 0.01)
        self.assertTrue(self.c1.render)
        self.assertTrue(self.c2.render)
        self.assertEqual(self.layer.bounds, Rect((10, 10), (40, 40)))

    def test_remove_child(self):
        self.layer._remove_child(self.c2)
        self.layer.update_logic(0.01)
        self.assertTrue(self.c1.logic)
        self.assertFalse(self.c2.logic)

    def test_destroy(self):
        self.layer.destroy()
        self.assertTrue(self.c1.destroyed)
        self.assertTrue(self.c2.destroyed)


class TestScene(unittest.TestCase):

    def setUp(self):
        self.scene = Scene()

    def test_bgm(self):
        sound = Sound('Music/Music.ogg')
        self.scene._bgm(sound)


class TestSceneManager(unittest.TestCase):
    class MockDrawContext(DrawContext):

        def __init__(self):
            pass

        def sub(self, origin):
            pass

        def blit(self, imagelike, xy: tuple):
            pass

        def circle(self, center, radius):
            pass

        def line(self, xy1, xy2):
            pass

        def fill(self, color):
            pass

    class MockScene(Scene):

        def __init__(self, outer):
            super().__init__()
            self.outer = outer

        def update_logic(self, dt):
            self.outer.logic += 1
            # Mesmo com esse evento, update_render ainda será chamado
            # porque a troca de cenas é "lazy" (só acontece quando dou tick)
            self._bus.emit(Event.SCENE_CHANGE, lambda: self.outer.second_scene)

        def update_render(self, draw_context: DrawContext, dt):
            self.outer.render += 1

        def destroy(self):
            self.outer.destroyed = True

    class SecondMockScene(Scene):

        def __init__(self, outer):
            self.outer = outer

        def update_logic(self, dt):
            self.outer.logic -= 1

        def update_render(self, draw_context: DrawContext, dt):
            self.outer.render -= 1

    def setUp(self):
        self.ctx = self.MockDrawContext()
        self.bus = EventBus()
        EventBus.active(self.bus)
        self.scene = self.MockScene(self)
        self.second_scene = self.SecondMockScene(self)
        self.mgr = SceneManager(self.ctx, self.bus, lambda: self.scene)
        self.logic = 0
        self.render = 0
        # Marca quando a MockScene é destruída, momento no qual
        # a SecondMockScene deve substituí-la
        self.destroyed = False

    def test_tick(self):
        self.mgr.tick(0.01)
        self.assertEqual(self.logic, 1)
        self.assertEqual(self.render, 1)
        self.mgr.tick(0.01)
        self.assertTrue(self.destroyed)
        self.assertEqual(self.logic, 0)
        self.assertEqual(self.render, 0)


class TestGameObject(unittest.TestCase):
    class MockScene(Scene):

        def __init__(self):
            super().__init__()
            self.cycles = {
                'logic': 0,
                'render': 0
            }

        def update_render(self, draw_context: DrawContext, dt):
            self.cycles['render'] += 1

        def update_logic(self, dt):
            self._bus.emit(Event.REQ_ANIM_FRAME)
            self.cycles['logic'] += 1
            if self.cycles['logic'] == 100:
                self._bus.emit(Event.QUIT, None)

    class MockDisplay(Display):

        def __init__(self):
            self.flipped = 0

        def draw_context(self):
            return TestSceneManager.MockDrawContext()

        def resolution(self, width, height):
            pass

        def flip(self):
            self.flipped += 1

    def create_scene(self):
        self.scene = self.MockScene()
        return self.scene

    def setUp(self):
        self.display = self.MockDisplay()
        # Atenção aqui ! Não posso instanciar uma Scene antes de GameObject,
        # porque este define um bus, enquanto a outra pede um bus
        self.game_object = GameObject(self.display, self.create_scene)

    def test_gameloop(self):
        self.game_object.gameloop()
        self.assertEqual(self.scene.cycles, {
            'logic': 100,
            'render': 100
        })
        self.assertEqual(self.display.flipped, 100)


if __name__ == '__main__':
    unittest.main()
