from .common import Stat


class Initiative(Stat):

    def __get__(self, instance, owner):
        result = instance.__dict__[self.name]
        for buff in instance.__dict__["effects"]:
            result += (buff.__dict__[self.stat] *
                       instance.__dict__[self.name])
        if result < 0.1:
            return 0.1
        else:
            return result


class Speed(Stat):

    pass
