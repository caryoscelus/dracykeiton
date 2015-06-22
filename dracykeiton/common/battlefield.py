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

from ..compat import *
from ..entity import Entity, listener

class SidedEntity(Entity):
    @unbound
    def _init(self, group=None):
        self.dynamic_property('ally_group', group)
    
    @unbound
    def is_enemy(self, other):
        if self.ally_group is None or other.ally_group is None:
            return False
        return self.ally_group != other.ally_group
    
    @unbound
    def is_ally(self, other):
        if self.ally_group is None or other.ally_group is None:
            return False
        return self.ally_group == other.ally_group

class BattlefieldEntity(Entity):
    @unbound
    def _init(self, field=None):
        self.dynamic_property('field', field)

class Side(Entity):
    @unbound
    def _init(self):
        self.req_mod(SidedEntity)
        self.dynamic_property('members', [])

class SimpleField(Entity):
    @unbound
    def _init(self, *args, **kwargs):
        keep_dead = kwargs.get('keep_dead')
        if keep_dead is None:
            keep_dead = True
        self.dynamic_property('sides', dict({side : Side() for side in args}))
        self.dynamic_property('keep_dead', keep_dead)
        # for saving/loading purpose
        for side in self.sides:
            for entity in self.sides[side].members:
                self.reg_entity(entity)
    
    @unbound
    def add_side(self, name, side):
        side.req_mod(SidedEntity, name)
        side.ally_group = name
        self.sides[name] = side
        for entity in side.members:
            self.reg_entity(entity)
    
    @unbound
    def spawn(self, side, entity):
        self.sides[side].members.append(entity)
        entity.be_born()
        self.reg_entity(entity)
        entity.req_mod(SidedEntity, side)
        entity.req_mod(BattlefieldEntity)
        entity.field = self
    
    @unbound
    def reg_entity(self, entity):
        entity.add_listener_node('living', self.remove_dead())
    
    @unbound
    def unspawn(self, entity):
        for side in self.sides:
            if entity in self.sides[side].members:
                self.sides[side].members.remove(entity)
    
    @unbound
    def get_enemies(self, side):
        return set(s for s in self.sides.keys() if self.sides[s] != side)
    
    @unbound
    def new_round(self):
        for side in self.sides:
            for entity in self.sides[side].members:
                try:
                    entity.new_round()
                except AttributeError:
                    pass
    
    @listener
    def remove_dead(self, target, value):
        if value == 'dead':
            if not self.keep_dead:
                self.unspawn(target)

class Battlefield(Entity):
    @unbound
    def _init(self, keep_dead=True):
        self.req_mod(SimpleField, 'left', 'right', keep_dead=keep_dead)
