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

"""
"""

from compat import *
from entity import Entity, listener

class SimpleField(Entity):
    @unbound
    def _init(self, *args):
        self.dynamic_property('sides', dict({side : [] for side in args}))
        # for saving/loading purpose
        for side in self.sides:
            for entity in self.sides[side]:
                self.reg_entity(entity)
    
    @unbound
    def spawn(self, side, entity):
        self.sides[side].append(entity)
        entity.be_born()
        self.reg_entity(entity)
    
    @unbound
    def reg_entity(self, entity):
        entity.add_listener_node('living', self.remove_dead())
    
    @unbound
    def unspawn(self, entity):
        for side in self.sides:
            if entity in self.sides[side]:
                self.sides[side].remove(entity)
    
    @unbound
    def get_enemies(self, side):
        return set(s for s in self.sides.keys() if s != side)
    
    @unbound
    def small_turn(self):
        for side in self.sides:
            for entity in self.sides[side]:
                entity.restore_ap()
    
    @listener
    def remove_dead(self, target, value):
        if value == 'dead':
            self.unspawn(target)

class Battlefield(Entity):
    @unbound
    def _init(self):
        self.add_mod(SimpleField, 'left', 'right')