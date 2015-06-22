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

from ..entity import Entity, simplenode, listener
from ..compat import *

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
    
    @unbound
    def die(self, msg='no reason'):
        self.living = 'dead'
    
    @unbound
    def be_born(self):
        if self.living == 'unborn':
            self.living = 'alive'
        elif self.living == 'dead':
            raise TypeError('dead cannot be born, try some black magic instead!')
        elif self.living == 'alive':
            raise TypeError('cannot be born twice!')

class HpEntity(Entity):
    @unbound
    def _init(self, maxhp=0):
        self.req_mod(LivingEntity)
        self.dynamic_property('hp', 0)
        self.dynamic_property('maxhp', maxhp)
        self.add_set_node('hp', self.hp_cap())
        self.add_listener_node('hp', self.check_hp())
        self.add_listener_node('living', self.check_if_born())
    
    @unbound
    def full_hp(self):
        self.hp = self.maxhp
    
    @unbound
    def hurt(self, damage):
        was_alive = self.living == 'alive'
        self.hp -= damage
        if was_alive and self.living == 'dead':
            return True
        return False
    
    @simplenode
    def hp_cap(self, value):
        return min(value, self.maxhp)
    
    @listener
    def check_hp(self, target, value):
        if self.hp <= 0:
            self.die('hp = {}'.format(self.hp))
    
    @listener
    def check_if_born(self, target, value):
        if value == 'alive':
            self.full_hp()

class RobustHpEntity(Entity):
    @unbound
    def _init(self, robust=1.0):
        self.req_mod(HpEntity)
        self.dynamic_property('robust', robust)
        self.add_get_node('maxhp', self.get_robust_hp())
    
    @simplenode
    def get_robust_hp(self, value):
        return value * self.robust

class LevelHpEntity(Entity):
    @unbound
    def _init(self):
        self.req_mod(HpEntity)
        self.add_get_node('maxhp', self.get_level_hp())
    
    @simplenode
    def get_level_hp(self, value):
        return value * (1+self.level/3)

class RoundingHpEntity(Entity):
    @unbound
    def _init(self):
        self.req_mod(HpEntity)
        self.add_set_node('hp', self.round_hp())
    
    @simplenode
    def round_hp(self, value):
        return int(value)
