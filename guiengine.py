import time
from enum import Enum
import pygame


def initialize(width, height):
    """
    Inicializa pygame, o backend da engine
    :param width: largura da tela (px)
    :param height: altura da tela (px)
    """
    pygame.display.init()
    pygame.font.init()
    # pygame.mixer.init()
    pygame.display.set_mode((width, height))


class EventBus:
    """
    Representa uma via de eventos, única durante a vida de uma sessão da engine.
    """
    __active = None

    @classmethod
    def active(cls, new_active=None):
        """
        Lê ou define a instância (singleton) ativa de `EventBus`
        :param new_active: Se não for `None`, causará substituição da instância ativa pela fornecida
        :return: A instância ativa de `EventBus`
        """
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
        """
        Define uma nova escuta de evento
        :param event_name: Nome do evento. Não precisa ser string, pode ser qualquer tipo. Basta que
        seja tratado como identificador de uma classe de eventos
        :param callback: Função a ser executada quando um evento da classe `event_name` for lançado.
        A função recebe um argumento contendo dados do evento (quem lança o evento é que define qual
        será esse argumento). A função não precisa retornar nada, mas, se retornar `True`, o `EventBus`
        não vai executar as outras funções de escuta (ou seja, retornar `True` equivale a pedir
        "cancelamento" do processamento do evento que foi lançado)
        """
        self.__ensure_exists(event_name)
        self._listeners[event_name].append(callback)

    def __disable_all_cbs(self, event_name):
        del self._listeners[event_name]

    def __disable_one_cb(self, event_name, callback):
        self._listeners[event_name].remove(callback)

    def disable(self, event_name, callback=None):
        """
        Desativa escutas
        :param event_name: Evento que se deseja parar de escutar
        :param callback: Função que não deve ser mais executada ao lançamento de `event_name`. Se vier
        como `None`, todas as escutas do evento serão desativadas
        """
        if callback is None:
            self.__disable_all_cbs(event_name)
        else:
            self.__disable_one_cb(event_name, callback)

    def disable_all(self):
        """
        Para de escutar todos os eventos
        """
        self._listeners.clear()

    def emit(self, event_name, event_data):
        """
        Lança/emite um evento da classe `event_name` com dados `event_data`
        :param event_name: Classe do evento a ser emitido
        :param event_data: Qualquer estrutura de dados representando dados associados ao evento sendo
        lançado
        """
        self.__ensure_exists(event_name)
        for callback in self._listeners[event_name]:
            if callback(event_data) is True:
                break


class BusProxy:
    """
    Funciona como `EventBus`. Um `BusProxy` é um "Proxy" (DP) para o `EventBus` ativo. Isso significa
    que chamar métodos de `BusProxy` vai delegar a métodos da instância ativa de `EventBus`.

    A diferença está na desativação: Chamar métodos de desativação implicará desativação somente
    de escutas registradas na mesma instância de `BusProxy`
    """
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
    """
    Um `EventBus` que lida com eventos originados fora dos componentes da engine
    (como cliques de mouse ou qualquer outra interação vinda do usuário)
    """
    def __init__(self):
        super().__init__()
        self.__redirection_target = None
        self.__emptyframes = 0
        self.__waited = []

    def redirect(self, target_bus):
        """
        Define a qual `EventBus` devem ser retransmitidos os eventos capturados por este `OuterBus`
        :param target_bus: Instância de `EventBus`
        """
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
    """"
    Lista de eventos definidos pela engine
    """
    QUIT = 'quit'
    MOUSEMOVE = 'mousemove'
    MOUSEDOWN = 'mousedown'
    MOUSEUP = 'mouseup'
    SCENE_CHANGE = 'scene-change'
    REQ_ANIM_FRAME = 'request-animation-frame'


class MouseAware:
    """
    É um facilitador de resposta a interações via mouse. Um `MouseAware` pode ser posto para observar
    um `EventBus`, caso no qual o `MouseAware` chamará seus métodos `onmouseenter`, `ondrag` etc. quando
    perceber que o comportamento do mouse é condizente.

    Para aproveitar a execução desses métodos (que são abstratos), defina subclasse de `MouseAware`
    """
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
        """
        Põe o `MouseAware` para ouvir uma instância de `EventBus`
        :param bus: Instância de `EventBus`
        :param bounds_lambda: Função que retorne um `Rect`, o qual será interpretado como a área
        da tela a ser monitorada pelo `MouseAware` (que assim perceberá quando o mouse entra na área,
        ou sai dela, etc.). A instância de `Rect` retornada pode variar ao longo do tempo
        """
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
    """
    Ver docs pygame
    """
    pass


class Surface(pygame.Surface):
    """
    Ver docs pygame
    """
    pass


class ResourceBank:
    """
    Um armazém de: imagens, sons, fontes.
    """
    current = None

    @classmethod
    def instance(cls):
        if cls.current is None:
            cls.current = ResourceBank()
        return cls.current

    def __init__(self):
        self.__bank = {}

    def image(self, path, cached=True):
        """
        Carrega uma imagem localizada em `path`, guardando-a numa memória cache caso `cached` seja `True`
        :param path: (string) Posição no sistema de arquivos onde a imagem está
        :param cached: (bool) Define se a imagem deve ser guardada em cache ou não. Se ela for, então
        próximas chamadas a este método feitas com o mesmo argumento `path` não irão mais carregar
        a imagem à memória, mas só retornar a versão guardada no cache
        :return: Instância de `Surface`
        """
        if self.__bank.get(path) is None:
            self.__bank[path] = pygame.image.load(path).convert_alpha()
        return self.__bank[path] if cached else pygame.image.load(path).convert_alpha()

    def sound(self, path, cached=True):
        """
        Análogo ao método `image`
        :return: Instância de `Sound` (pygame)
        """
        if self.__bank.get(path) is None:
            self.__bank[path] = pygame.mixer.Sound(path)
        return self.__bank[path] if cached else pygame.mixer.Sound(path)

    def __localfont(self, fontname, size):
        return str(fontname) + ':size:' + str(size)

    def font(self, fontname, size, cached=True):
        """
        Análogo ao método `image`
        :param fontname: Nome da fonte
        :param size: (int) tamanho da fonte
        :param cached: Análogo ao método `image`
        :return: Instância de `Font` (pygame)
        """
        if self.__bank.get(self.__localfont(fontname, size)) is None:
            self.__bank[self.__localfont(fontname, size)] = pygame.font.Font(fontname, size)
        return self.__bank[self.__localfont(fontname, size)] if cached \
            else pygame.font.Font(fontname, size)


class Image:
    """
    Representa uma imagem e possibilita operá-la (mudar tamanho, etc.)
    """
    def __init__(self, path):
        """

        :param path: Posição da imagem do sistema de arquivos
        """
        self.__path = path
        self.__surf = ResourceBank.instance().image(path)
        self.__update_virtuals()
        self.__factor = 1

    def __update_virtuals(self):
        self.width = self.__surf.get_width()
        self.height = self.__surf.get_height()

    def scale(self, factor):
        """
        Aumenta ou diminui tamanho
        :param factor: (int) fator multiplicativo
        :return: self (modificação é "in-place")
        """
        self.__factor *= factor
        self.__surf = pygame.transform.smoothscale(
            self.__surf,
            (int(self.__surf.get_width() * factor), int(self.__surf.get_height() * factor))
        )
        self.__update_virtuals()
        return self

    def clone(self, apply_changes=True):
        """
        Clona a imagem atual (cópia é desvinculada da original mesmo a nível de ponteiros)
        :param apply_changes: (bool) Define se transformações a esta `Image` durante sua vida útil devem
        ser aplicadas no clone também
        :return: Instância de `Image`
        """
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
        """
        Degrada um nível de abstração, retornando o objeto `Surface` subjacente a este objeto
        :return: Instância de `Surface`
        """
        return self.__surf


class Text:
    """
    Representa um texto e permite operá-lo (trocar mensagem, cor e tamanho)
    """
    def __init__(self, content, size, font, color, background):
        """

        :param content: Mensagem do texto (ou seja, uma string)
        :param size: (int) Tamanho
        :param font: (string) Nome da fonte
        :param color: Uma tupla de 3 inteiros, definindo cor da letra no sistema RGB
        :param background: Uma tupla de 3 inteiros, definindo cor do fundo no sistema RGB
        """
        self.__content = content
        self.__color = color
        self.__size = size
        self.__fontfamily = font
        self.__font = pygame.font.Font(font, size)
        self.__dirty = True
        self.__surf = None
        self.__background = background

    def color(self, color_tuple):
        """
        Muda cor da letra
        :param color_tuple: Tupla de 3 inteiros (RGB)
        """
        if self.__color != color_tuple:
            self.__color = color_tuple
            self.__dirty = True

    def content(self, string=None):
        """
        Muda mensagem do texto
        :param string: Nova mensagem
        """
        if string is None:
            return self.__content
        if self.__content != string:
            self.__content = string
            self.__dirty = True

    def size(self, newsize=None):
        """
        Lê ou altera o tamanho do texto (um inteiro)
        :param newsize: (int) Novo tamanho para o texto. Se vier como `None`, o tamanho não será alterado
        e o método retornará o tamanho atual
        :return: Caso `newsize` venha como `None`, o tamanho atual do texto (um int). Caso contrário,
        `None`
        """
        if newsize is None:
            return self.__size
        self.__size = newsize
        self.__font = pygame.font.Font(self.__fontfamily, newsize)
        self.__dirty = True

    def width(self):
        """
        Lê largura do texto (px)
        :return: (int)
        """
        return self.__font.size(self.__content)[0]

    def height(self):
        """
        Lê altura do texto (px)
        :return: (int)
        """
        return self.__font.size(self.__content)[1]

    def to_surface(self):
        """
        Degrada um nível de abstração, retornando o objeto `Surface` subjacente a este `Text`
        :return: Instância de `Surface`
        """
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
    """
    Representa um som e permite tocá-lo (com repetição ou não) e pará-lo
    """
    def __init__(self, path):
        """
        :param path: Localização do arquivo de som no sistema de arquivos
        """
        self.__sound = ResourceBank.instance().sound(path)
        self.__channel = None

    def play(self, repeat=0):
        """
        Toca o som
        :param repeat: um inteiro representando quantas vezes o som deve ser repetido. 0 significa
        infinitas vezes
        :return: self (para chain)
        """
        if self.__channel is not None:
            self.__channel.play(self.__sound, repeat)
        else:
            self.__channel = self.__sound.play(repeat)
        return self

    def stop(self):
        """
        Para de tocar o som
        :return: self (para chain)
        """
        if self.__channel is not None:
            self.__channel.stop()
        return self


class EmptySound:
    """
    DP (NullObject). É um som que pode ser tocado e parado, mas que, em qualquer caso, não vai fazer nada
    """
    def play(self, repeat=0):
        return self

    def stop(self):
        return self


class DrawContext:
    """
    Objeto por meio do qual é possível desenhar na tela. Uma instância de `DrawContext` é criada
    a partir de outra instância, que é tomada como "raiz" da nova. Isso possibilita criar uma
    hierarquia de instâncias de `DrawContext`, cada uma possivelmente transladada em relação à outra
    """
    def __init__(self, root_context, origin):
        """

        :param root_context: Instância de `DrawContext` da qual este objeto é derivado
        :param origin: Tupla (x,y) representando a origem do sistema de coordenadas deste objeto
        em relação ao `root_context`
        """
        self.__root = root_context
        self.__origin = origin

    def blit(self, imagelike, xy: tuple):
        """
        Desenha qualquer objeto que tenha o método `tosurface` na posição `xy` (sistema de coordenadas
        local a este objeto).
        :param imagelike: Qualquer objeto que tenha o método `tosurface` adequado (como `Image` e `Text`)
        :param xy: Tupla (x,y) onde deve ser desenhado o `imagelike`. As coordenadas são em relação ao
        sistema de coordenadas desta instância de `DrawContext`, não em relação à tela absoluta
        :return: Instância de `Rect` representando a porção de tela onde foi feito o desenho.
        As coordenas deste `Rect` (x e y) são globais em relação ao topo esquerdo da tela
        """
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
        """
        Cria um `DrawContext` hierarquicamente embaixo do atual.
        :param origin: Tupla (x,y) especificando a origem do sistema de coordenadas do novo `DrawContext`,
        em relação ao sistema de coordenadas do `DrawContext` atual
        :return: Instância de `DrawContext`
        """
        return DrawContext(self.__root,
                           tuple(l1 + l2 for l1, l2 in zip(self.__origin, origin)))

    def fill(self, color):
        """
        Desnecessário
        :param color:
        :return:
        """
        pass


class RootDrawContext(DrawContext):
    """
    O `DrawContext` original, que realmente desenha na tela (todos os outros `DrawContext`,
    hierarquicamente inferiores a este, simplesmente delegam a este).
    """
    def __init__(self, surface):
        """

        :param surface: Instância de surface representando a tela
        """
        # A origem de um DrawContext é relativa ao RootDrawContext (por isso o (0,0))
        super().__init__(self, (0, 0))
        self.__surface = surface

    def blit(self, imagelike, xy):
        return self.__surface.blit(imagelike.to_surface(), xy)

    def fill(self, color):
        """
        Preenche a tela toda com uma cor
        :param color: Tupla (r,g,b)
        """
        self.__surface.fill(color)


class Display:
    """
    Representa a janela gráfica
    """
    def __init__(self, width, height):
        """

        :param width: (int) largura (px)
        :param height: (int) altura (px)
        """
        self.__ctx = None
        pygame.display.init()
        self.resolution(width, height)

    def resolution(self, width, height):
        """
        Troca resolução da tela
        :param width: (int)
        :param height: (int)
        """
        pygame.display.set_mode((width, height))
        self.__ctx = RootDrawContext(pygame.display.get_surface())

    def draw_context(self):
        """
        Cria um `DrawContext` que permite desenhar na janela gráfica representada por este objeto
        :return: Instância de `DrawContext` (concretamente, instância de `RootDrawContext`, mas os
        métodos de interesse estão na superclasse)
        """
        return self.__ctx

    def flip(self):
        """
        Atualiza a janela gráfica para refletir operações de desenho que tenham sido realizadas.
        Em outras palavras, chamar métodos de desenho não mudará a imagem na tela. As modificações
        só serão observáveis quando `flip` for chamado.
        :return:
        """
        pygame.display.flip()


class Renderizable:
    """
    Componente básico da engine. Representa qualquer objeto que será desenhado na tela.

    Possui um membro `_bus` para acessar o `EventBus` compartilhado por todos os componentes da engine
    """
    def __init__(self, xy):
        """

        :param xy: Tupla (x,y) representando a posição do canto esquerdo superior
        """
        self.bounds = Rect(xy, (0, 0))
        self._bus = BusProxy()
        self.__xy = xy

    def xy(self, point=None):
        """
        Redefine a posição do objeto
        :param point: Tupla (x,y)
        """
        if point is None:
            return self.__xy
        self.__xy = point

    def update_render(self, draw_context: DrawContext, dt):
        """
        Método abstrato. Deve desenhar o objeto na tela
        :param draw_context: Instância de `DrawContext`
        :param dt: (number) tempo decorrido desde a última atualização de componentes no loop gráfico
        """
        pass

    def update_logic(self, dt):
        """
        Método abstrato. Deve atualizar propriedades (arbitrárias) do objeto
        :param dt: (number) Tempo decorrido desde a última atualização de componentes no loop gráfico
        """
        pass

    def destroy(self):
        """
        Destrói o componente. Isso desativará todas as suas escutas.
        """
        self._bus.disable_all()


class FigureNode(Renderizable):
    """
    Componente desenhável originado de uma imagem
    """

    def __init__(self, xy, image):
        """

        :param xy: Ver `Renderizable`
        :param image: Instância de `Image`
        """
        super().__init__(xy)
        self.__image = image
        # Não adianta fazer isso, porque a origem continuará relativa, não absoluta
        # self.bounds = image.get_rect()

    def set_image(self, image):
        """
        Troca a imagem
        :param image: Instância de `Image`
        """
        self.__image = image

    def update_render(self, draw_context: DrawContext, dt):
        """
        Desenha o objeto na tela. Como é um `FigureNode`, isso corresponde a desenhar a imagem dele
        na tela.
        """
        self.bounds = draw_context.blit(self.__image, self.xy())


class TextNode(Renderizable):
    """
    Componente desenhável originado de um texto
    """
    def __init__(self, xy, text):
        """

        :param xy: Ver `Renderizable`
        :param text: Instância de `Text`
        """
        super().__init__(xy)
        self.__text = text

    def size(self, newsize=None):
        """
        Troca tamanho do texto
        :param newsize: (int)
        """
        return self.__text.size(newsize)

    def update_render(self, draw_context: DrawContext, dt):
        """
        Desenha texto na tela
        """
        self.bounds = draw_context.blit(self.__text, self.xy())


class ButtonNode(TextNode):
    """
    Componente representando um botão com texto clicável
    """
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
        """
        Define a função a ser executada quando do clique do botão
        :param callback: Função a ser executada quando o botão for clicado
        """
        self._callback.append(callback)


class Layer(Renderizable):
    """
    Componente abstrato da engine. É uma "âncora" que abriga vários subcomponentes desenháveis,
    formando uma árvore de renderização
    """
    def __init__(self, xy):
        super().__init__(xy)
        self.__children = []

    def _add_child(self, renderizable):
        """
        Adiciona um filho à àrvore de renderização, diretamente abaixo deste objeto
        :param renderizable: Instância de `Renderizable`
        """
        self.__children.append(renderizable)

    def _remove_child(self, renderizable):
        """
        Retira filho da árvore de renderização
        :param renderizable: Instância de `Renderizable`
        """
        renderizable.destroy()
        self.__children.remove(renderizable)

    def update_render(self, draw_context: DrawContext, dt):
        """
        Desenha o objeto na tela. Como é um `Layer`, na verdade chama o `update_render` de todos
        os filhos
        """
        for child in self.__children:
            # self.xy() é relativo ao draw_context fornecido a esta Layer, então OK
            child.update_render(draw_context.sub(self.xy()), dt)
        if len(self.__children) == 0:
            self.bounds = Rect(self.xy(), (0, 0))
        else:
            self.bounds = self.__children[0].bounds.unionall(
                [x.bounds for x in self.__children])

    def update_logic(self, dt):
        """
        Atualiza a lógica de todos os filhos
        """
        for child in self.__children:
            child.update_logic(dt)

    def destroy(self):
        """
        Destrói a si e a todos os filhos
        """
        super().destroy()
        for child in self.__children:
            child.destroy()
        self.__children.clear()


class Scene(Layer):
    """
    Componente abstrato da engine. Sua intenção é definir um "estado de jogo", ou seja, tudo o
    que aparece na tela num determinado momento.

    Para usá-la, crie subclasse e implemente o método abstrato `_parts`
    """
    def __init__(self):
        super().__init__((0, 0))
        self.__bgm = EmptySound()
        self.__background = (0, 0, 0)
        self._parts()

    def update_render(self, draw_context: DrawContext, dt):
        draw_context.fill(self.__background)
        super().update_render(draw_context, dt)

    def _background(self, background):
        """
        Muda cor do plano de fundo da tela
        :param background: (r,g,b)
        """
        self.__background = background

    def _bgm(self, sound: Sound):
        """
        Define um som como "background music"
        :param sound: Instância de `Sound`
        """
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
    """
    Objeto que conhece a cena de jogo atual (tutorial, menu principal, etc, a depender do jogo
    concretamente implementado a partir das classes abstratas da engine) e sabe como trocar de cena
    (porém, o pedido para mudar vem do usuário, quando este emite um evento `Event.SCENE_CHANGE`)
    """

    def __init__(self, draw_context, bus, initial_scene):
        """

        :param draw_context: Instância de `DrawContext` para desenho na tela. Todos os componentes
        gráficos da cena (toda a árvore de renderização) fará uso desse `draw_context`
        :param bus: Instância de `EventBus`, a ser usada para comunicação por todos os compoenentes
        gráficos da árvore de renderização
        :param initial_scene: Não é uma instância, mas uma classe. Deve ser uma subclasse de `Scene`,
        definindo a primeira cena do jogo
        """
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
        """
        Causa atualização na árvore de renderização inteira
        :param dt: Tempo decorrido desde a última atualização
        """
        self.__check_change_scene()
        self.__current.update_logic(dt)
        self.__current.update_render(self.__ctx, dt)

    def destroy(self):
        """
        Destrói a cena sendo administrada atualmente. Só é útil para finalizar o jogo, porque trocar
        de cena é feito mediante eventos, não destruindo a cena atual (mesmo porque não há método
        para criar cena nova)
        """
        self.__current.destroy()


class GameObject:
    """
    Representa o jogo inteiro, com a janela gráfica e o gerenciador de cenas
    """
    def __init__(self, display, initial_scene):
        """

        :param display: Instância de `Display`
        :param initial_scene: Não é uma instância, mas uma classe. Deve ser subclasse de `Scene`,
        e define a cena na qual o jogo começa
        """
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
        """
        Gera um loop infinito de atualização do jogo.
        """
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
