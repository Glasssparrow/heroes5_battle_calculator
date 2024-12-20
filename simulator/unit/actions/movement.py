from .common import Action
from ...simulator_keywords import JUST_MOVEMENT


class Movement(Action):

    def __init__(self, owner):
        super().__init__(owner)
        self.type_of_action = JUST_MOVEMENT
