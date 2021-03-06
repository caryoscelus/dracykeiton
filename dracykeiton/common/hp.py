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

from ..compat import *
from ..entity import Entity, simplenode, listener, depends, mod_dep
from .level import Level

class Living(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('living', 'unborn')
    
    @unbound
    def _load(self):
        self.add_set_node('living', self.ensure_correct())
    
    @simplenode
    def ensure_correct(value):
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
    
    @unbound
    def be_unborn(self):
        if self.living != 'dead':
            self.living = 'unborn'

@mod_dep(Living)
class Hp(Entity):
    @unbound
    def _init(self, maxhp=0):
        self.dynamic_property('hp', 0, priorities=('normal', 'round'))
        self.dynamic_property('maxhp', maxhp, priorities=('normal', 'round'))
    
    @unbound
    def _load(self):
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
    
    @depends('maxhp')
    @simplenode
    def hp_cap(value, maxhp):
        return min(value, maxhp)
    
    @listener
    def check_hp(self, target, value):
        if self.hp <= 0:
            self.die('hp = {}'.format(self.hp))
    
    @listener
    def check_if_born(self, target, value):
        if value == 'alive':
            self.full_hp()

@mod_dep(Hp)
class RobustHp(Entity):
    @unbound
    def _init(self, robust=1.0):
        self.dynamic_property('robust', robust)
    
    @unbound
    def _load(self):
        self.add_get_node('maxhp', self.get_robust_hp())
    
    @depends('robust')
    @simplenode
    def get_robust_hp(value, robust):
        return value * robust

@mod_dep(Hp, Level)
class LevelHp(Entity):
    @unbound
    def _init(self):
        pass
    
    @unbound
    def _load(self):
        self.add_get_node('maxhp', self.get_level_hp())
    
    @depends('level')
    @simplenode
    def get_level_hp(value, level):
        return value * (1+level/3)

@mod_dep(Hp)
class RoundingHp(Entity):
    @unbound
    def _init(self):
        pass
    
    @unbound
    def _load(self):
        self.add_set_node('hp', self.round_hp(), priority='round')
        self.add_get_node('maxhp', self.round_hp(), priority='round')
    
    @simplenode
    def round_hp(value):
        return int(value)
