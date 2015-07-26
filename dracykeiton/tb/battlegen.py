##
##  Copyright (C) 2015 caryoscelus
##
##  This file is part of Dracykeiton
##  https://github.com/caryoscelus/dracykeiton
##  
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##  
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

"""BattleGen: generate battle encounters"""

from ..compat import *
from .. import random
from ..common.battlefield import Battlefield, Side
import copy

class SideGen(object):
    def __init__(self, name, controller, amount, predefined=list(), possible=list()):
        super(SideGen, self).__init__()
        if not hasattr(amount, '__getitem__'):
            amount = (amount, amount)
        self.name = name
        self.controller = controller
        self.predefined = predefined
        self.possible = possible
        self.amount = amount
    
    def generate(self):
        entities = copy.copy(self.predefined)
        if len(entities) > self.amount[1]:
            raise IndexError('too much predefined entities ({} > {})'.format(len(entities), self.amount[1]))
        if not self.possible and len(entities) < self.amount[0]:
            raise IndexError('not enough predefined entities and no possible ({} < {})'.format(len(entities), self.amount[0]))
        length = max(len(entities), random.randint(*self.amount))
        while length > len(entities):
            entity = random.choice(self.possible)()
            entities.append(entity)
        return entities

class BattleGen(object):
    def __init__(self, turnman_c, **battlefield_args):
        super(BattleGen, self).__init__()
        self.sides = []
        self.battlefield_args = battlefield_args
        self.turnman_c = turnman_c
    
    def add_side(self, *args, **kwargs):
        self.sides.append(SideGen(*args, **kwargs))
    
    def generate(self):
        """Generate encounter (returns turnman)"""
        battlefield = Battlefield(**self.battlefield_args)
        turnman = self.turnman_c(battlefield)
        for side_gen in self.sides:
            side = Side()
            battlefield.add_side(side_gen.name, side)
            controller = side_gen.controller(battlefield, side)
            turnman.add_side(controller)
            entities = side_gen.generate()
            for entity in entities:
                battlefield.spawn(side_gen.name, entity)
        return turnman
