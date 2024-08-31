from math import floor


class Stat:

    def __set_name__(self, owner, name):
        self.name = "_" + name
        self.stat = name

    def __get__(self, instance, owner):
        result = instance.__dict__[self.name]
        for buff in instance.__dict__["effects"]:
            result += buff.__dict__[self.stat]
        result = floor(result)
        if result < 0:
            return 0
        else:
            return result

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
