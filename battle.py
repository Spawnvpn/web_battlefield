"""""""""
This module implements the logic of the battle between the armies.
First we need to specify the number of armies, the number of units
of each army, the number of units in the unit of each army and the
strategy of fighting each army. After starting 2 random army that
would fight each other will be selected. Logic armies battle consists
in choosing the enemy army unit according to the strategy and attack
the last chance of the current army squad.
After the victory of one army over 2 random selected and the cycle repeats.
"""""""""

from units import *


class Squad(object):

    def __init__(self, number_of_units):
        self.number_of_units = number_of_units
        self.units = list()
        self.get_units()
        self.power = self.get_power()
        self.active = True

    def get_units(self):
        if self.number_of_units > 10:
            self.number_of_units = 10
        elif self.number_of_units < 5:
            self.number_of_units = 5
        for _ in range(0, self.number_of_units):
            self.units.append(random.choice([Solder(), Vehicle()]))

    def is_active_units(self):
        active_units = list()
        for unit in self.units:
            if unit.active:
                active_units.append(unit)
        return active_units

    def get_power(self):
        squad_power = float()
        self.units = self.is_active_units()
        for unit in self.units:
            squad_power += unit.do_attack() / len(self.units)
        return squad_power

    def take_damage(self, mutual_damage):
        if mutual_damage != 0 and len(self.units) != 0:
            damage = mutual_damage / len(self.units)
        else:
            damage = 0
        for unit in self.units:
            unit.take_damage(damage)
        self.units = self.is_active_units()
        if len(self.units) == 0:
            self.active = False


class Army(object):

    def __init__(self, number_of_squads, number_of_units, strategy):
        self.number_of_squads = number_of_squads
        self.number_of_units = number_of_units
        self.squads = list()
        self.get_squads()
        self.strategy = strategy
        self.active = True

    def get_squads(self):
        if self.number_of_squads > 50:
            self.number_of_squads = 50
        elif self.number_of_squads < 2:
            self.number_of_squads = 2
        for _ in range(0, self.number_of_squads):
            self.squads.append(Squad(self.number_of_units))

    def get_strategy(self, army):
        if self.strategy == "random":
            random.shuffle(army.squads)

        elif self.strategy == "weakest":
            for squad in army.squads:
                for every in army.squads:
                    if every.power < squad.power:
                        buff = army.squads[army.squads.index(squad)]
                        army.squads[army.squads.index(squad)] = every
                        army.squads[army.squads.index(every)] = buff

        elif self.strategy == "strongest":
            for squad in army.squads:
                for every in army.squads:
                    if every.power > squad.power:
                        buff = army.squads[army.squads.index(squad)]
                        army.squads[army.squads.index(squad)] = every
                        army.squads[army.squads.index(every)] = buff

    def active_squads(self):
        active_squads = list()
        for squad in self.squads:
            if squad.active:
                active_squads.append(squad)
        return active_squads

    def attack(self, army):
        self.get_strategy(army)
        if len(army.squads) != 0:
            for squad in army.squads:
                squad.take_damage(self.squads[
                    self.squads.index(random.choice(self.squads))].get_power())
            self.squads = self.active_squads()
            if len(self.squads) == 0:
                self.active = False


class Battlefield(object):

    def __init__(self, armies_active=True, winner=None, **kwargs):
        self.armies_active = armies_active
        self.quan_armies = kwargs['quan_armies']
        self.units = kwargs['units']
        self.squads = kwargs['squads']
        self.strategy = kwargs['strategy']
        self.winner = winner

    def start(self):
        armies = list()
        for x in range(self.quan_armies):
            number_of_units = self.units[x]
            number_of_squads = self.squads[x]
            strategy = self.strategy[x]
            x = Army(number_of_units, number_of_squads, strategy)
            armies.append(x)
        while self.armies_active:
            some_army = armies[armies.index(random.choice(armies))]
            some_else_army = armies[armies.index(random.choice(armies))]
            if some_army != some_else_army:
                while some_army.active and some_else_army.active:
                    some_army.attack(some_else_army)
                    some_else_army.attack(some_army)
            self.is_active_armies(armies)

    def is_active_armies(self, armies):
        count_inactive_armies = int()
        for army in armies:
            if not army.active:
                count_inactive_armies += 1
        if count_inactive_armies == len(armies) - 1:
            for win in armies:
                if win.active:
                    # print("Army %s win!" % (armies.index(win) + 1))
                    self.winner = "Army %s win!" % (armies.index(win) + 1)
                    self.armies_active = False
        return

armies_packed = False
armies_quantity = None
i = 0
squads = []
units = []
strategy = []
