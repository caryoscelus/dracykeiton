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

"""Hit action"""

from ..compat import *
from ..entity import Entity, simplenode, depends, mod_dep
from ..action import action
from .ap import ActionPointEntity
from .inspire import InspirableEntity
from .kill import KillingEntity
from .accuracy import Accuracy
from .. import random

@mod_dep(ActionPointEntity, KillingEntity, Accuracy)
class HittingEntity(Entity):
    @unbound
    def _init(self, hit_damage=0):
        self.dynamic_property('hit_damage', hit_damage)
    
    @action
    def hit(self, enemy):
        if self.try_hit(enemy):
            self.force_hit(enemy)
    
    @unbound
    def try_hit(self, enemy):
        try:
            evasion = enemy.evasion
        except AttributeError:
            evasion = -1
        accuracy = self.accuracy
        return accuracy > evasion
    
    @unbound
    def force_hit(self, enemy):
        killed = enemy.hurt(self.hit_damage)
        if killed:
            self.killed(enemy)
    
    @unbound
    def can_hit(self, enemy):
        return self.spend_ap(2)

@mod_dep(InspirableEntity, HittingEntity)
class InspirableHittingEntity(Entity):
    @unbound
    def _init(self):
        pass
    
    @unbound
    def _load(self):
        self.add_get_node('hit_damage', self.inspired_damage())
    
    @depends('inspired')
    @simplenode
    def inspired_damage(value, inspired):
        if inspired:
            return value * 2
        return value

@mod_dep(HittingEntity)
class RandomHittingEntity(Entity):
    @unbound
    def _init(self):
        pass
    
    @unbound
    def _load(self):
        self.add_get_node('hit_damage', self.randomize_hit())
    
    @simplenode
    def randomize_hit(value):
        # 1+-1/3
        return (random.random()+1)*2/3.0*value
