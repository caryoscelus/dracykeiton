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

from entity import Entity, EntityMod
from controller import Controller
from turnman import Turnman

class HpEntity(EntityMod):
    def __init__(self, maxhp=1):
        self.default_maxhp = maxhp
    
    def enable(self, target):
        target.dynamic_property('hp', empty=0)
        target.dynamic_property('maxhp')
        target.maxhp = self.default_maxhp
        target.dynamic_method('full_hp')
        target.full_hp = type(self).full_hp
        target.dynamic_method('hurt')
        target.hurt = type(self).hurt
    
    def full_hp(self):
        self.hp = self.maxhp
    
    def hurt(self, damage):
        self.hp -= damage

class ActionPointEntity(EntityMod):
    def __init__(self, ap=0):
        super(ActionPointEntity, self).__init__()
        self.default_ap = ap
    
    def enable(self, target):
        target.dynamic_property('ap', empty=0)
        target.dynamic_property('maxap', empty=self.default_ap)
        target.dynamic_method('spend_ap')
        target.spend_ap = type(self).spend_ap
        target.dynamic_method('restore_ap')
        target.restore_ap = type(self).restore_ap
    
    def spend_ap(self, ap):
        if self.ap < ap:
            return False
        else:
            self.ap -= ap
            return True
    
    def restore_ap(self):
        self.ap = self.maxap

class HitEnemyAction(EntityMod):
    def __init__(self, hit=0):
        self.default_hit = hit
    
    def enable(self, target):
        target.dynamic_property('hit_damage')
        target.hit_damage = self.default_hit
        target.dynamic_method('hit')
        target.hit = type(self).hit
    
    def hit(self, enemy):
        if self.spend_ap(2):
            enemy.hurt(self.hit_damage)

class Goblin(Entity):
    def __init__(self):
        super(Goblin, self).__init__()
        self.add_mod(HpEntity(4))
        self.add_mod(ActionPointEntity(3))
        self.add_mod(HitEnemyAction(2))

class SimpleField(EntityMod):
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
            assert entity.hit_damage == 2
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
    hurted = [entity for entity in right_side.entities if entity.hp < 4]
    assert hurted != []
