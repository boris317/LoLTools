#
class DamageReduction(object):
    def __init__(self, amount):
        self.amount = amount
     
    def effective_health(self, health):
        if self.amount >= 0:
            return health * (100.0 + self.amount) / 100.0
        elif self.amount < 0:
            return health * 100.0 / (100.0 + abs(self.amount))  
                    
    def mitigate(self, damage, defense_penetration=None):
        #returns damage actually dealt after applying the damage multiplier
        amount = self.amount
        if defense_penetration:
            if defense_penetration.reduction_percent:
                amount -= (amount * defense_penetration.reduction_percent)
            if defense_penetration.reduction:
                amount -= defense_penetration.reduction
            if amount > 0 and defense_penetration.penetration_percent:
                self.amount -= (amount * defense_penetration.penetration_percent)
                if self.amount < 0:
                    self.amount = 0
            if amount > 0 and defense_penetration.penetration:
                amount -= defense_penetration.penetration
                if amount < 0:
                    amount = 0 

        return damage * self.multiplier(amount)
    
    def apply_hit(self, hit):
        return self.mitigate(hit.amount, hit.defense_penetration)
    
    def multiplier(self, amount=None):
        if amount is None:
            amount = self.amount

        if amount >= 0:
            return 100.0 / (100.0 + amount)
        elif amount < 0:
            return 1.0 + abs(amount) / 100.0        
    
class DefensePenetration(object):
    def __init__(self, reduction_percent=None, reduction=None, 
                 penetration_percent=None, penetration=None):
        self.reduction_percent = reduction_percent
        self.reduction = reduction
        self.penetration = penetration
        self.penetration_percent = penetration_percent
        
class Hit(object):
    def __init__(self, amount, defense_penetration=None):
        self.amount = amount
        self.defense_penetration = defense_penetration
    