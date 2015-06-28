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

"""Leveling up attributes"""

from ..compat import *
from ..entity import Entity, mod_dep, simplenode, depends
from ..action import action
from .dexterity import Dexterity
from .level import LevelAbility

@mod_dep(LevelAbility)
class AttributeLevelup(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('level_points', 0)
        self.dynamic_property('spent_level_points', 0)
        self.dynamic_property('attribute_levelup', set())
    
    @unbound
    def _load(self):
        self.add_get_node('level_points', self.get_level_points())
    
    @action
    def increase_attribute(self, attribute):
        setattr(self, attribute, getattr(self, attribute)+1)
    
    @unbound
    def can_increase_attribute(self, attribute):
        if attribute in self.attribute_levelup:
            return self.spend_level_points(1)
        return False
    
    @unbound
    def spend_level_points(self, amount):
        if self.level_points >= amount:
            self.spent_level_points += amount
            return True
        return False
    
    @unbound
    def add_levelup_attribute(self, attribute):
        self.attribute_levelup.add(attribute)
    
    @depends('spent_level_points', 'level')
    @simplenode
    def get_level_points(value, spent_level_points, level):
        return level-spent_level_points
