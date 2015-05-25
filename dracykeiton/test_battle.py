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

""""Real-world" test: jrpg-style two-side battle
"""

import copy
import random

from entity import Entity
from controller import Controller
from turnman import Turnman
from ap import ActionPointEntity
from hp import HpEntity, HittingEntity
from compat import *

class Goblin(Entity):
    @unbound
    def _init(self):
        self.add_mod(HpEntity, 5)
        self.add_mod(ActionPointEntity, 4)
        self.add_mod(HittingEntity, 3)

class SimpleField(Entity):
    @unbound
    def _init(self, *args):
        self.sides = dict({side : [] for side in args})
        self.dynamic_property('sides')
    
    @unbound
    def spawn(self, side, entity):
        self.sides[side].append(entity)
        entity.full_hp()
    
    @unbound
    def get_enemies(self, side):
        return set(s for s in self.sides.keys() if s != side)
    
    @unbound
    def small_turn(self):
        for side in self.sides:
            for entity in self.sides[side]:
                entity.restore_ap()

class Battlefield(Entity):
    @unbound
    def _init(self):
        self.add_mod(SimpleField, 'left', 'right')

class AIBattleController(Controller):
    def __init__(self, world, side):
        super(AIBattleController, self).__init__(world)
        self.side = side
    
    def act(self):
        enemy_sides = self.world.get_enemies(self.side)
        side = random.choice(tuple(enemy_sides))
        enemies = self.world.sides[side]
        enemy = enemies[0]
        for entity in self.entities:
            hp = enemy.hp
            entity.hit(enemy)
            assert enemy.hp != hp

def prepare_battle():
    battlefield = Battlefield()
    left_side = AIBattleController(battlefield, 'left')
    right_side = AIBattleController(battlefield, 'right')
    for i in range(2):
        goblin = Goblin()
        left_side.add_entity(goblin)
        battlefield.spawn('left', goblin)
    for i in range(3):
        goblin = Goblin()
        right_side.add_entity(goblin)
        battlefield.spawn('right', goblin)
    turnman = Turnman(battlefield)
    turnman.add_side(left_side)
    turnman.add_side(right_side)
    return turnman

def test_battle():
    turnman = prepare_battle()
    turnman.turn()
    right_side = turnman.sides[1]
    hurted = [entity for entity in right_side.entities if entity.hp < 5]
    assert hurted != []
    assert hurted[0].hp == -1