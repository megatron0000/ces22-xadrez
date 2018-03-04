import pygame


class EventBus:
    __active = None

    @classmethod
    def active(cls, new_active=None):
        if new_active is None:
            return cls.__active
        else:
            cls.__active = new_active

    def __init__(self):
        self._listeners = {}

    def __ensure_exists(self, event_name):
        if self._listeners.get(event_name) is None:
            self._listeners[event_name] = []

    def on(self, event_name, callback):
        self.__ensure_exists(event_name)
        self._listeners[event_name].append(callback)

    def __disable_all_cbs(self, event_name):
        del self._listeners[event_name]

    def __disable_one_cb(self, event_name, callback):
        self._listeners[event_name].remove(callback)

    def disable(self, event_name, callback=None):
        if callback is None:
            self.__disable_all_cbs(event_name)
        else:
            self.__disable_one_cb(event_name, callback)

    def disable_all(self):
        self._listeners.clear()

    def emit(self, event_name, event_data):
        self.__ensure_exists(event_name)
        for callback in self._listeners[event_name]:
            callback(event_data)


class BusProxy:

    def __init__(self):
        self._listeners = {}
        self._proxied_bus = EventBus.active()

    def __ensure_exists(self, event_name):
        if self._listeners.get(event_name) is None:
            self._listeners[event_name] = []

    def on(self, event_name, callback):
        self.__ensure_exists(event_name)
        self._listeners[event_name].append(callback)
        self._proxied_bus.on(event_name, callback)

    def __disable_all_cbs(self, event_name):
        del self._listeners[event_name]

    def __disable_one_cb(self, event_name, callback):
        self.__ensure_exists(event_name)
        self._listeners[event_name].remove(callback)

    def disable(self, event_name, callback=None):
        if callback is None:
            self.__disable_all_cbs(event_name)
        else:
            self.__disable_one_cb(event_name, callback)
        self._proxied_bus.disable(event_name, callback)

    def disable_all(self):
        for event, cb_list in self._listeners.items():
            for cb in cb_list:
                self._proxied_bus.disable(event, cb)
        self._listeners.clear()

    def emit(self, event_name, event_data):
        # Ops, should only delegate
        # self.__ensure_exists(event_name)
        # for callback in self._listeners[event_name]:
        #     callback(event_data)
        self._proxied_bus.emit(event_name, event_data)


class Rect(pygame.Rect):
    pass


class Surface(pygame.Surface):
    pass


class ResourceBank:
    current = None

    @classmethod
    def instance(cls):
        if cls.current is None:
            cls.current = ResourceBank()
        return cls.current

    def __init__(self):
        self.__bank = {}

    def image(self, path, cached=True):
        if self.__bank.get(path) is None:
            self.__bank[path] = pygame.image.load(path).convert_alpha()
        return self.__bank[path] if cached else pygame.image.load(path).convert_alpha()


class Image:

    def __init__(self, path):
        self.__surf = ResourceBank.instance().image(path)
        self.__update_virtuals()

    def __update_virtuals(self):
        self.width = self.__surf.get_width()
        self.height = self.__surf.get_height()

    def scale(self, factor):
        self.__surf = pygame.transform.smoothscale(
            self.__surf,
            (int(self.__surf.get_width() * factor), int(self.__surf.get_height() * factor))
        )
        self.__update_virtuals()
        return self

    def rotate(self, degrees):
        """
        Desnecessário
        :param degrees:
        :return:
        """
        pass

    def to_surface(self):
        return self.__surf


class DrawContext:

    def __init__(self, root_context, origin):
        self.__root = root_context
        self.__origin = origin

    def blit(self, image, xy: tuple):
        return self.__root.blit(image,
                                tuple(l1 + l2 for l1, l2 in zip(xy, self.__origin)))

    def line(self, xy1, xy2):
        """
        Desnecessário
        :param xy1:
        :param xy2:
        :return:
        """
        pass

    def circle(self, center, radius):
        """
        Desnecessário
        :param center:
        :param radius:
        :return:
        """
        pass

    def sub(self, origin):
        return DrawContext(self.__root,
                           tuple(l1 + l2 for l1, l2 in zip(self.__origin, origin)))


class RootDrawContext(DrawContext):

    def __init__(self, origin, surface):
        # A origem de um DrawContext é relativa ao RootDrawContext (por isso o (0,0))
        super().__init__(self, (0, 0))
        self.__origin = origin
        self.__surface = surface

    def blit(self, image, xy):
        return self.__surface.blit(image.to_surface(),
                                   tuple(l1 + l2 for l1, l2 in zip(self.__origin, xy)))


class Renderizable:

    def __init__(self):
        self.bounds = Rect((0, 0), (0, 0))

    def update_render(self):
        # IMPLEMENTAR !
        pass
