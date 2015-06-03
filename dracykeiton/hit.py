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

from compat import *
from entity import Entity
from ap import LivingActingEntity, ActionPointEntity

class HittingEntity(Entity):
    @unbound
    def _init(self, hit_damage=0):
        self.add_mod(ActionPointEntity)
        self.add_mod(LivingActingEntity)
        self.dynamic_property('hit_damage', hit_damage)
    
    @unbound
    def hit(self, enemy):
        if self.spend_ap(2):
            enemy.hurt(self.hit_damage)
