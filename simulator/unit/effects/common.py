

class Effect:

    def __init__(self):
        self.name = "default"
        self.attack = 0
        self.defence = 0
        self.damage = 0
        self.initiative = 0
        self.speed = 0
        self.luck = 0
        self.morale = 0
        self.time = 0
        self.initiative_mark = None
        self.special_effects = []
        self.modifiers = {}
        self.have_timer = False
        self.blocked_by_immunities = []
        self.dispell_conditions = []
        self.dispell_exception_once = False
        self.is_aura = False

    def reapply(self, new_instance):
        self.time = new_instance.time
