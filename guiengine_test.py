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


class TestRootDrawContext(unittest.TestCase):

    def setUp(self):
        self.ctx = RootDrawContext((20, 10), Surface((500, 500)))
        self.img = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png') \
            .scale(1 / 10)

    def test_blit(self):
        rect = self.ctx.blit(self.img, (30, 30))
        self.assertEqual(rect.x, 20 + 30)
        self.assertEqual(rect.y, 10 + 30)


class TestDrawContext(unittest.TestCase):

    def setUp(self):
        initpygame()
        self.root = RootDrawContext((20, 10), Surface((500, 500)))
        self.img = Image('resources/Cburnett V2 improved/PNGs/square brown dark_png.png') \
            .scale(1 / 10)

    def test_sub_blit(self):
        sub = self.root.sub((40, 40)).sub((60, 60))
        rect = sub.blit(self.img, (50, 50))
        self.assertEqual(rect.x, 20 + 40 + 60 + 50)
        self.assertEqual(rect.y, 10 + 40 + 60 + 50)


if __name__ == '__main__':
    unittest.main()
