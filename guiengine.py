import time
from enum import Enum
import pygame


def initialize(width, height):
    pygame.display.init()
    pygame.font.init()
    # pygame.mixer.init()
    pygame.display.set_mode((width, height))


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
            if callback(event_data) is True:
                break


class BusProxy:

    def __init__(self):
        self._listeners = {}
        self._proxied_bus = EventBus.active()
        if self._proxied_bus is None:
            raise RuntimeError('No bus exists. Are you requesting ' +
                               'a BusProxy outside the scene environment ?')

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

    def emit(self, event_name, event_data=None):
        # Só redireciona ao bus original
        self._proxied_bus.emit(event_name, event_data)


class OuterBus(EventBus):

    def __init__(self):
        super().__init__()
        self.__redirection_target = None
        self.__emptyframes = 0
        self.__waited = []

    def redirect(self, target_bus):
        self.__redirection_target = target_bus

    def emit(self, event_name, event_data):
        if self.__redirection_target is not None:
            self.__redirection_target.emit(event_name, event_data)
        else:
            super().emit(event_name, event_data)

    def wait(self):
        """
        Bloqueia a thread corrente até que haja evento novo do pygame
        """
        self.__waited = [pygame.event.wait()]

    def refresh(self):
        """
        Processa todos os eventos do pygame coletados,
        inclusive aquele que tenha sido esperado por self.wait()
        """
        for event in self.__waited + pygame.event.get():
            self.__process_event(event)
        self.__waited = []
        pygame.time.wait(0)

    def __process_event(self, event):
        if event.type == pygame.QUIT:
            self.emit(Event.QUIT, None)
        elif event.type == pygame.MOUSEMOTION:
            self.emit(Event.MOUSEMOVE, event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.emit(Event.MOUSEDOWN, event.pos)
        # elif second button or middle button, emit other events
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.emit(Event.MOUSEUP, event.pos)
        # Teclas, por enquanto, não são necessárias


class Event(Enum):
    QUIT = 'quit'
    MOUSEMOVE = 'mousemove'
    MOUSEDOWN = 'mousedown'
    MOUSEUP = 'mouseup'
    SCENE_CHANGE = 'scene-change'
    REQ_ANIM_FRAME = 'request-animation-frame'


class MouseAware:

    def __init__(self):
        self.__bounds_lambda = None
        self.__mousedown_at = None
        self.__mouseinside = False
        self.__isdragging = False

    def __onmousedown(self, data):
        self.__mousedown_at = data

    def __onmouseup(self, data):
        if self.__mousedown_at is None:
            return
        # click
        if abs(data[0] + data[1] - (self.__mousedown_at[0] + self.__mousedown_at[1])) < 10 \
                and self.__bounds_lambda().collidepoint(self.__mousedown_at):
            self.onclick()
        # dragend
        if self.__isdragging is True:
            self.ondragend(data)
            self.__isdragging = False
        # Incondicionalmente deletar mousedown_at
        self.__mousedown_at = None

    def __onmousemove(self, data):
        # mouseenter e mouseleave
        # (talvez tenha que restringir a somente enquanto não estiver acontecendo um drag)
        mouseinside = bool(self.__bounds_lambda().collidepoint(data))
        if mouseinside is True and self.__mouseinside is False:
            self.onmouseenter()
        elif mouseinside is False and self.__mouseinside is True:
            self.onmouseleave()
        self.__mouseinside = mouseinside
        # dragstart
        if self.__mousedown_at is not None and self.__isdragging is False:
            was_inside = bool(self.__bounds_lambda().collidepoint(self.__mousedown_at))
            if was_inside:
                self.ondragstart(self.__mousedown_at)
                self.__isdragging = True
        if self.__mousedown_at is not None and self.__isdragging is True:
            self.ondrag(data)

    def watch(self, bus, bounds_lambda):
        self.__bounds_lambda = bounds_lambda
        bus.on(Event.MOUSEDOWN, self.__onmousedown)
        bus.on(Event.MOUSEUP, self.__onmouseup)
        bus.on(Event.MOUSEMOVE, self.__onmousemove)

    def onclick(self):
        pass

    def onmouseenter(self):
        pass

    def onmouseleave(self):
        pass

    def ondragstart(self, pos):
        pass

    def ondrag(self, pos):
        pass

    def ondragend(self, pos):
        pass


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

    def sound(self, path, cached=True):
        if self.__bank.get(path) is None:
            self.__bank[path] = pygame.mixer.Sound(path)
        return self.__bank[path] if cached else pygame.mixer.Sound(path)

    def __localfont(self, fontname, size):
        return str(fontname) + ':size:' + str(size)

    def font(self, fontname, size, cached=True):
        if self.__bank.get(self.__localfont(fontname, size)) is None:
            self.__bank[self.__localfont(fontname, size)] = pygame.font.Font(fontname, size)
        return self.__bank[self.__localfont(fontname, size)] if cached \
            else pygame.font.Font(fontname, size)


class Image:

    def __init__(self, path):
        self.__path = path
        self.__surf = ResourceBank.instance().image(path)
        self.__update_virtuals()
        self.__factor = 1

    def __update_virtuals(self):
        self.width = self.__surf.get_width()
        self.height = self.__surf.get_height()

    def scale(self, factor):
        self.__factor *= factor
        self.__surf = pygame.transform.smoothscale(
            self.__surf,
            (int(self.__surf.get_width() * factor), int(self.__surf.get_height() * factor))
        )
        self.__update_virtuals()
        return self

    def clone(self, apply_changes=True):
        out = Image(self.__path)
        if apply_changes:
            out.scale(self.__factor)
        return out

    def rotate(self, degrees):
        """
        Desnecessário
        :param degrees:
        :return:
        """
        pass

    def to_surface(self):
        return self.__surf


class Text:

    def __init__(self, content, size, font, color, background):
        self.__content = content
        self.__color = color
        self.__size = size
        self.__fontfamily = font
        self.__font = pygame.font.Font(font, size)
        self.__dirty = True
        self.__surf = None
        self.__background = background

    def color(self, color_tuple):
        if self.__color != color_tuple:
            self.__color = color_tuple
            self.__dirty = True

    def content(self, string=None):
        if string is None:
            return self.__content
        if self.__content != string:
            self.__content = string
            self.__dirty = True

    def size(self, newsize=None):
        if newsize is None:
            return self.__size
        self.__size = newsize
        self.__font = pygame.font.Font(self.__fontfamily, newsize)
        self.__dirty = True

    def width(self):
        return self.__font.size(self.__content)[0]

    def height(self):
        return self.__font.size(self.__content)[1]

    def to_surface(self):
        if self.__dirty:
            self.__surf = self.__font.render(
                self.__content, True, self.__color + (0,))
            surf = pygame.Surface(tuple(l * 1.2 for l in self.__surf.get_size()))
            surf.fill(self.__background)
            surf.blit(self.__surf, tuple(l * 0.1 for l in self.__surf.get_size()))
            self.__surf = surf
            self.__dirty = False
        return self.__surf


class Sound:

    def __init__(self, path):
        self.__sound = ResourceBank.instance().sound(path)
        self.__channel = None

    def play(self, repeat=0):
        if self.__channel is not None:
            self.__channel.play(self.__sound, repeat)
        else:
            self.__channel = self.__sound.play(repeat)
        return self

    def stop(self):
        if self.__channel is not None:
            self.__channel.stop()
        return self


class EmptySound:

    def play(self, repeat=0):
        return self

    def stop(self):
        return self


class DrawContext:

    def __init__(self, root_context, origin):
        self.__root = root_context
        self.__origin = origin

    def blit(self, imagelike, xy: tuple):
        return self.__root.blit(imagelike,
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

    def fill(self, color):
        pass


class RootDrawContext(DrawContext):

    def __init__(self, surface):
        # A origem de um DrawContext é relativa ao RootDrawContext (por isso o (0,0))
        super().__init__(self, (0, 0))
        self.__surface = surface

    def blit(self, imagelike, xy):
        return self.__surface.blit(imagelike.to_surface(), xy)

    def fill(self, color):
        self.__surface.fill(color)


class Display:

    def __init__(self, width, height):
        self.__ctx = None
        pygame.display.init()
        self.resolution(width, height)

    def resolution(self, width, height):
        pygame.display.set_mode((width, height))
        self.__ctx = RootDrawContext(pygame.display.get_surface())

    def draw_context(self):
        return self.__ctx

    def flip(self):
        pygame.display.flip()


class Renderizable:

    def __init__(self, xy):
        self.bounds = Rect(xy, (0, 0))
        self._bus = BusProxy()
        self.__xy = xy

    def xy(self, point=None):
        if point is None:
            return self.__xy
        self.__xy = point

    def update_render(self, draw_context: DrawContext, dt):
        pass

    def update_logic(self, dt):
        pass

    def destroy(self):
        self._bus.disable_all()


class FigureNode(Renderizable):

    def __init__(self, xy, image):
        super().__init__(xy)
        self.__image = image
        # Não adianta fazer isso, porque a origem continuará relativa, não absoluta
        # self.bounds = image.get_rect()

    def set_image(self, image):
        self.__image = image

    def update_render(self, draw_context: DrawContext, dt):
        self.bounds = draw_context.blit(self.__image, self.xy())


class TextNode(Renderizable):

    def __init__(self, xy, text):
        super().__init__(xy)
        self.__text = text

    def size(self, newsize=None):
        return self.__text.size(newsize)

    def update_render(self, draw_context: DrawContext, dt):
        self.bounds = draw_context.blit(self.__text, self.xy())


class ButtonNode(TextNode):
    class MouseInButton(MouseAware):

        def __init__(self, outer):
            self.outer = outer
            super().__init__()

        def onmouseenter(self):
            self.outer.size(int(self.outer.size() * 1.15))

        def onmouseleave(self):
            self.outer.size(int(self.outer.size() / 1.15))

        def onclick(self):
            for i in self.outer._callback:
                i()

    def __init__(self, xy, text):
        super().__init__(xy, text)
        self.MouseInButton(self).watch(self._bus, lambda: self.bounds)
        self._callback = []

    def onclick(self, callback):
        self._callback.append(callback)


class Layer(Renderizable):

    def __init__(self, xy):
        super().__init__(xy)
        self.__children = []

    def _add_child(self, renderizable):
        self.__children.append(renderizable)

    def _remove_child(self, renderizable):
        renderizable.destroy()
        self.__children.remove(renderizable)

    def update_render(self, draw_context: DrawContext, dt):
        for child in self.__children:
            # self.xy() é relativo ao draw_context fornecido a esta Layer, então OK
            child.update_render(draw_context.sub(self.xy()), dt)
        if len(self.__children) == 0:
            self.bounds = Rect(self.xy(), (0, 0))
        else:
            self.bounds = self.__children[0].bounds.unionall(
                [x.bounds for x in self.__children])

    def update_logic(self, dt):
        for child in self.__children:
            child.update_logic(dt)

    def destroy(self):
        super().destroy()
        for child in self.__children:
            child.destroy()
        self.__children.clear()


class Scene(Layer):

    def __init__(self):
        super().__init__((0, 0))
        self.__bgm = EmptySound()
        self.__background = (0, 0, 0)
        self._parts()

    def update_render(self, draw_context: DrawContext, dt):
        draw_context.fill(self.__background)
        super().update_render(draw_context, dt)

    def _background(self, background):
        self.__background = background

    def _bgm(self, sound: Sound):
        self.__bgm.stop()
        self.__bgm = sound
        self.__bgm.play(-1)

    def destroy(self):
        super().destroy()
        self.__bgm.stop()

    def _parts(self):
        """
        Classes filhas devem se construir aqui (devem chamar _add_child() etc aqui)
        :return: Qualquer coisa, porque o retorno será desprezado
        """
        pass


class SceneManager:

    def __init__(self, draw_context, bus, initial_scene):
        self.__ctx = draw_context
        self.__bus = bus
        self.__requested_scene = None
        self.__current = initial_scene()
        self.__bus.on(Event.SCENE_CHANGE, self.__event_listener)

    def __event_listener(self, data):
        self.__requested_scene = data

    def __check_change_scene(self):
        if self.__requested_scene is not None:
            self.__current.destroy()
            self.__current = self.__requested_scene()
            self.__requested_scene = None

    def tick(self, dt):
        self.__check_change_scene()
        self.__current.update_logic(dt)
        self.__current.update_render(self.__ctx, dt)

    def destroy(self):
        self.__current.destroy()


class GameObject:

    def __init__(self, display, initial_scene):
        self.__display = display
        self.__outer_bus = OuterBus()
        self.__bus = EventBus()
        EventBus.active(self.__bus)
        self.__bus.on(Event.QUIT, self.__quit_listener)
        self.__bus.on(Event.REQ_ANIM_FRAME, self.__req_anim_frame_listener)
        self.__outer_bus.redirect(self.__bus)
        self.__scene_mgr = SceneManager(display.draw_context(), self.__bus, initial_scene)
        self.__should_stop = False
        self.__should_wait = True

    def __quit_listener(self, data):
        self.__should_stop = True

    def __req_anim_frame_listener(self, data):
        self.__should_wait = False

    def gameloop(self):
        time_now = time.clock()
        while not self.__should_stop:
            if self.__should_wait:
                self.__outer_bus.wait()
            self.__should_wait = True
            self.__outer_bus.refresh()
            time_before = time_now
            time_now = time.clock()
            dt = time_now - time_before
            if dt < 1 / 60:
                time.sleep(1 / 60 - dt)
            if dt > 20 * 1 / 60:
                dt = 1 / 60
            self.__scene_mgr.tick(dt)
            self.__display.flip()
        self.__scene_mgr.destroy()
