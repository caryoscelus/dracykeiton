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
from ..entity import Entity, simplenode
from ..action import action
from .ap import LivingActingEntity, ActionPointEntity
from .. import random

class HittingEntity(Entity):
    @unbound
    def _init(self, hit_damage=0):
        self.req_mod(ActionPointEntity)
        self.req_mod(LivingActingEntity) # ?
        self.dynamic_property('hit_damage', hit_damage)
    
    @action
    def hit(self, enemy):
        enemy.hurt(self.hit_damage)
    
    @unbound
    def can_hit(self, enemy):
        return self.spend_ap(2)

class RandomHittingEntity(Entity):
    @unbound
    def _init(self):
        self.req_mod(HittingEntity)
        self.add_get_node('hit_damage', self.randomize_hit())
    
    @simplenode
    def randomize_hit(self, value):
        # 1+-1/3
        return (random.random()+1)*2/3.0*value
