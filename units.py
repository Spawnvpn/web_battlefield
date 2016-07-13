"""""""""
This module implements the behavior of the logic units and their parameters.
"""""""""

import time
import random


class Unit(object):

    def __init__(self, health=100, recharge=float(), recharge_state=True,
                 recharge_time=0, experience=0.0, active=True):
        self.health = health
        self.recharge = recharge
        self.recharge_state = recharge_state
        self.recharge_time = recharge_time
        self.experience = experience
        self.active = active

    def get_recharge(self):
        if self.recharge_time < time.time():
            return True
        else:
            return False


class Solder(Unit):

    def __init__(self, **kwargs):
        super(Solder, self).__init__(**kwargs)
        self.recharge = random.randint(100.0, 2000.0)
        self.armour = float()

    def do_attack(self):
        self.recharge_state = self.get_recharge()
        if self.recharge_state:
            damage = 15 * (1 + self.health / 100) * random.randrange(
                50 + self.experience, 101) / 100
            if self.experience < 50:
                self.experience += 1
            self.recharge_time = time.time() + self.recharge * 10 ** -3
            return damage
        elif not self.recharge_state:
            return 0

    def get_armour(self):
        self.armour = 0.05 + self.experience / 100
        return self.armour / 2

    def take_damage(self, damage):
        if damage - self.armour < 0:
            return
        self.health -= (damage - self.get_armour())
        if self.health <= 0:
            self.active = False


class Vehicle(Unit):

    def __init__(self, **kwargs):
        super(Vehicle, self).__init__(**kwargs)
        self.operators = list()
        for _ in range(0, random.randrange(2, 3)):
            self.operators.append(Solder())
        self.recharge = random.randrange(1000, 2000)
        self.health = self.get_health()
        self.armour = self.get_armour()

    def get_operators_damage(self):
        operators_damage = float()
        for operator in self.operators:
            operators_damage += operator.do_attack()
        if operators_damage == 0.0:
            return 0
        average = operators_damage / len(self.operators)
        return average

    def get_health(self):
        health_operators = float()
        for operator in self.operators:
            health_operators += operator.health
        health = health_operators + 100 / len(self.operators)
        return health

    def do_attack(self):
        recharge_state = self.get_recharge()
        if recharge_state:
            damage = 20 * (1 + self.health / 100) * self.get_operators_damage()
            if self.experience < 50:
                self.experience += 1
            self.recharge_time = time.time() + self.recharge * 10 ** -3
            return damage
        elif not recharge_state:
            return 0

    def active_operators(self):
        active_operators = list()
        for operator in self.operators:
            if operator.active:
                active_operators.append(operator)
        return active_operators

    def get_armour(self):
        def calc_experience():
            exp = float()
            for operator in self.operators:
                exp += operator.experience
            return exp

        self.armour = 0.05 + calc_experience() / 100
        return self.armour / 2

    def take_damage(self, damage):
        if damage - self.armour < 0:
            return
        self.health -= ((damage * 0.6) - self.armour)
        oper_amount = len(self.operators)
        self.operators[0].health -= damage * 0.2
        self.operators[random.randint(0, oper_amount-1)].health -= damage * 0.1
        self.operators[random.randint(0, oper_amount-1)].health -= damage * 0.1
        self.operators = self.active_operators()
        if self.health <= 0 or len(self.operators) == 0:
            self.active = False
