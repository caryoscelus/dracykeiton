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
    
    @unbound
    def empty_side(self):
        return all([member.living != 'alive' for member in self.members])

class BattleState(object):
    pass

class NotFinished(BattleState):
    def __str__(self):
        return 'Not finished'

class Finished(BattleState):
    def __str__(self):
        return 'Finished'

class Won(Finished):
    def __init__(self, winner):
        self.winner = winner
    
    def __str__(self):
        return 'Won by {}'.format(self.winner)

class SimpleField(Entity):
    @unbound
    def _init(self, *args, **kwargs):
        keep_dead = kwargs.get('keep_dead', True)
        self.dynamic_property('sides', dict())
        self.dynamic_property('win_conditions', dict())
        self.dynamic_property('lose_conditions', dict())
        self.dynamic_property('keep_dead', keep_dead)
        self.dynamic_property('state', NotFinished())
        for side in args:
            if not side in self.sides:
                self.add_side(side, Side())
        # for saving/loading purpose
        for side in self.sides:
            for entity in self.sides[side].members:
                self.reg_entity(entity)
    
    @unbound
    def add_side(self, name, side):
        side.req_mod(SidedEntity, name)
        side.ally_group = name
        self.sides[name] = side
        self.win_conditions[name] = set()
        self.lose_conditions[name] = set()
        for entity in side.members:
            self.reg_entity(entity)
    
    @unbound
    def add_lose_condition(self, side, cond):
        self.lose_conditions[side].add(cond)
    
    @unbound
    def add_win_condition(self, side, cond):
        self.win_conditions[side].add(cond)
    
    @unbound
    def check_conditions(self):
        result = dict()
        for side in self.sides:
            for lose in self.lose_conditions[side]:
                if lose(self.sides[side]):
                    result[side] = 'lose'
                    break
            else:
                for win in self.win_conditions[side]:
                    if win(self.sides[side]):
                        result[side] = 'win'
                        break
        if len(result) == len(self.sides):
            winners = [side for side in result if result[side] == 'win']
            if winners:
                self.state = Won(winners)
            else:
                self.state = Finished()
        elif len(result)+1 == len(self.sides):
            winners = [side for side in result if result[side] == 'win']
            if winners:
                self.state = Won(winners)
            else:
                self.state = Won([side for side in self.sides if not side in result])
    
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
    
    @unbound
    def new_turn(self):
        self.check_conditions()
    
    @listener
    def remove_dead(self, target, value):
        if value == 'dead':
            if not self.keep_dead:
                self.unspawn(target)

class Battlefield(Entity):
    @unbound
    def _init(self, keep_dead=True):
        self.req_mod(SimpleField, 'left', 'right', keep_dead=keep_dead)
