import time


class A:

    def dosomething(self):
        pass


class B:

    def dosomething(self):
        pass


class C:
    def dosomething(self):
        raise TypeError


arrayc = [A() if i % 2 == 0 else B() for i in range(10000)]
arrayn = [1 if i % 2 == 0 else 2 for i in range(10000)]

before = time.clock()
for turn in range(1000):
    for i in arrayc:
        i.dosomething()
now = time.clock()
print('polymorphism:', (now - before), 'ms per loop')

before = time.clock()
for turn in range(1000):
    for i in arrayc:
        if i == 1:
            pass
        elif i == 2:
            pass
now = time.clock()
print('if:', (now - before), 'ms per loop', '\n')

arrayc = [A() if i % 10 != 0 else C() for i in range(10000)]

before = time.clock()
for turn in range(1000):
    for i in arrayc:
        try:
            i.dosomething()
        except TypeError:
            pass
now = time.clock()
print('polymorphism:', (now - before), 'ms per loop')

before = time.clock()
for turn in range(1000):
    for i in arrayc:
        if isinstance(i, A):
            i.dosomething()
now = time.clock()
print('if:', (now - before), 'ms per loop', '\n')


class D:

    def __init__(self):
        self.kind = self.__class__


class E(D):
    pass


arrayc = arrayc = [D() if i % 2 == 0 else E() for i in range(10000)]

before = time.clock()
for turn in range(1000):
    for i in arrayc:
        if isinstance(i, E):
            pass
        elif isinstance(i, D):
            pass
now = time.clock()
print('isinstance:', (now - before), 'ms per loop')

before = time.clock()
for turn in range(1000):
    for i in arrayc:
        if i.kind is D:
            pass
        elif i.kind is E:
            pass
now = time.clock()
print('obj.kind is:', (now - before), 'ms per loop')

before = time.clock()
for turn in range(1000):
    for i in arrayc:
        if i.kind == D:
            pass
        elif i.kind == E:
            pass
now = time.clock()
print('obj.kind ==:', (now - before), 'ms per loop')
