import random
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.random = random.choice(list(range(1000)))


a = Singleton()
b = Singleton()
print(a is b)
a.a= "chicken"
print(b.a)


class B(object):
    def __init__(self):
        self.single = Singleton()
        self.single.deck = [1,2,3]

b1 = B()
b2 = B()

print(b1.single.a)
print(a.deck)
print(a.random)
print(b1.single.random)
