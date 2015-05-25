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

"""Hit point system"""

from entity import Entity, simplenode
from compat import *

class LivingEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('living', 'unborn')
        self.add_set_node('living', self.ensure_correct())
    
    @simplenode
    def ensure_correct(self, value):
        if not value in ('unborn', 'alive', 'dead'):
            raise TypeError('living property cannnot equal "{}"'.format(value))
        return value

class HpEntity(Entity):
    @unbound
    def _init(self, maxhp=0):
        self.add_mod(LivingEntity)
        self.dynamic_property('hp', 0)
        self.dynamic_property('maxhp', maxhp)
    
    @unbound
    def full_hp(self):
        self.hp = self.maxhp
    
    @unbound
    def hurt(self, damage):
        self.hp -= damage

class HittingEntity(Entity):
    @unbound
    def _init(self, hit_damage=0):
        self.dynamic_property('hit_damage', hit_damage)
    
    @unbound
    def hit(self, enemy):
        if self.spend_ap(2):
            enemy.hurt(self.hit_damage)
