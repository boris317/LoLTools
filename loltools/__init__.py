#
class DamageReduction(object):
    #amount of damage reduction points
    def __set_amount(self, amount):
        self.__amount = float(amount)
        self.__damage_multiplier = 100.0 / (100.0 + self.__amount)
    def __get_amount(self):
        return self.__amount
    amount = property(__get_amount, __set_amount)
    
    #percent of damage reduced
    def __get_multiplier(self):
        return self.__damage_multiplier
    multiplier = property(__get_multiplier)
    
    def __init__(self, amount):
        self.__damage_multiplier = None
        self.__amount = None
        self.amount = amount
        
    def mitigate(self, damage, defense_reduction=None):
        #returns damage actually dealt after applying the damage multiplier
        orig_amount  = self.amount
        if defense_reduction:
            if defense_reduction.defense_reduction_percent:
                self.amount -= (self.amount * defense_reduction.defense_reduction_percent)
            if defense_reduction.defense_reduction:
                self.amount -= defense_reduction.defense_reduction
            if self.amount > 0 and defense_reduction.defense_pen_percent:
                self.amount -= (self.amount * defense_reduction.defense_pen_percent)
                if self.amount < 0:
                    self.amount = 0
            if self.amount > 0 and defense_reduction.defense_pen:
                self.amount -= defense_reduction.defense_pen
                if self.amount < 0:
                    self.amount = 0 
        
        final_damage = damage * self.multiplier
        self.amount = orig_amount
        return final_damage
    
    def apply_hit(self, hit):
        return self.mitigate(hit.amount, hit)
    
class Hit(object):
    def __init__(self, amount, defense_reduction_percent=None, defense_reduction=None, 
                 defense_pen_percent=None, defense_pen=None):
        self.amount = amount
        self.defense_reduction_percent = defense_reduction_percent
        self.defense_reduction = defense_reduction
        self.defense_pen_percent = defense_pen_percent
        self.defense_pen = defense_pen
    