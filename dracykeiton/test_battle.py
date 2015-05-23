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

class HpEntity(Entity):
    def init(self):
        self.dynamic_property('hp', empty=0)
        self.dynamic_property('maxhp', empty=0)
        #self.dynamic_method('full_hp')
        #self.dynamic_method('hurt')
    
    def full_hp(self):
        self.hp = self.maxhp
    
    def hurt(self, damage):
        self.hp -= damage

class ActionPointEntity(Entity):
    def init(self):
        self.dynamic_property('ap', empty=0)
        self.dynamic_property('maxap', empty=0)
        #target.dynamic_method('spend_ap')
        #target.dynamic_method('restore_ap')
    
    def spend_ap(self, ap):
        if self.ap < ap:
            return False
        else:
            self.ap -= ap
            return True
    
    def restore_ap(self):
        self.ap = self.maxap

class HitEnemyAction(Entity):
    def init(self):
        self.dynamic_property('hit_damage', empty=0)
        #self.dynamic_method('hit')
    
    def hit(self, enemy):
        if self.spend_ap(2):
            enemy.hurt(self.hit_damage)

class Goblin(Entity):
    def init(self):
        self.add_mod(HpEntity)
        self.add_mod(ActionPointEntity)
        self.add_mod(HitEnemyAction)
        self.maxap = 4
        self.hit_damage = 3
        self.maxhp = 5

class SimpleField(Entity):
    def __init__(self, *args):
        super(SimpleField, self).__init__()
        self.sides = {side : [] for side in args}
    
    def enable(self, target):
        target.dynamic_property('sides')
        target.sides = copy.deepcopy(self.sides)
        target.dynamic_method('spawn')
        target.spawn = type(self).spawn
        target.dynamic_method('get_enemies')
        target.get_enemies = type(self).get_enemies
        target.dynamic_method('small_turn')
        target.small_turn = type(self).small_turn
    
    def spawn(self, side, entity):
        self.sides[side].append(entity)
        entity.full_hp()
    
    def get_enemies(self, side):
        return set(s for s in self.sides.keys() if s != side)
    
    def small_turn(self):
        for side in self.sides:
            for entity in self.sides[side]:
                entity.restore_ap()

class Battlefield(Entity):
    def __init__(self):
        super(Battlefield, self).__init__()
        self.add_mod(SimpleField('left', 'right'))

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

def test_battle():
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
    turnman.turn()
    hurted = [entity for entity in right_side.entities if entity.hp < 5]
    assert hurted != []
    assert hurted[0].hp == -1
