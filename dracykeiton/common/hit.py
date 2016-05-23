##
##  Copyright (C) 2015-2016 caryoscelus
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
from ..entity import Entity, simplenode, depends, mod_dep, properties, data_node
from ..action import action, category
from .actor import ActionChance
from .ap import ActionPoint
from .inspire import Inspirable
from .kill import Kill
from .accuracy import Accuracy
from .. import random

@mod_dep(ActionPoint, Kill, Accuracy)
@properties(hit_damage=0)
class Hit(Entity):
    @category('battle')
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
        return accuracy >= evasion
    
    @unbound
    def force_hit(self, enemy):
        killed = enemy.hurt(self.hit_damage)
        if killed:
            self.killed(enemy)
    
    @unbound
    def can_hit(self, enemy):
        return self.spend_ap(2)

@mod_dep(Inspirable, Hit)
class InspirableHit(Entity):
    @unbound
    def _load(self):
        self.add_get_node('hit_damage', self.inspired_damage())
    
    @depends('inspired')
    @simplenode
    def inspired_damage(value, inspired):
        if inspired:
            return value * 2
        return value

@mod_dep(Hit)
class RandomHit(Entity):
    @unbound
    def _load(self):
        self.add_get_node('hit_damage', self.randomize_hit())
    
    @simplenode
    def randomize_hit(value):
        # 1+-1/3
        return (random.random()+1)*2/3.0*value

@properties(
    hit_chance=1.0,
    hit_damage=0,
    crit_chance=1.0,
)
class Hurt(Entity):
    pass

@mod_dep(Hit, ActionChance, Hurt)
@data_node('get', 'action_chance', deps=['hit_chance'])
def HitAction(value, hit_chance):
    return hit_chance
