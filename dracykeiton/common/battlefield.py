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

"""
"""

from ..compat import *
from ..entity import Entity, listener, mod_dep, properties
from ..tb import battle
from .hp import Living
from .turn import TurnEntity

@properties(ally_group=None)
class Sided(Entity):
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

@properties(field=None)
class BattlefieldEntity(Entity):
    pass

@mod_dep(Sided)
@properties(members=list)
class Side(Entity):
    @unbound
    def empty_side(self):
        return all([member.living != 'alive' for member in self.members])

@properties(
    sides=dict,
    to_reg=list,
)
class SidedCombat(Entity):
    @unbound
    def _load(self):
        # for saving/loading purpose
        self.to_reg = list(self.sides.keys())
        self.ensure_registration()
    
    @unbound
    def ensure_registration(self):
        to_reg = list()
        for side in self.to_reg:
            try:
                for entity in self.sides[side].members:
                    self.reg_entity(entity)
            except AttributeError:
                to_reg.append(side)
        self.to_reg = to_reg
    
    @unbound
    def add_side(self, name, side):
        self.ensure_registration()
        side.add_mod(Sided, ally_group=name)
        self.sides[name] = side
        self.win_conditions[name] = set()
        self.lose_conditions[name] = set()
        for entity in side.members:
            self.reg_entity(entity)

@mod_dep(SidedCombat)
class WinLoseConditions(Entity):
    @unbound
    def _init(self, win_conditions=dict(), lose_conditions=dict()):
        self.dynamic_property('win_conditions', win_conditions)
        self.dynamic_property('lose_conditions', lose_conditions)
    
    @unbound
    def add_lose_condition(self, side, cond):
        self.lose_conditions[side].add(cond)
    
    @unbound
    def add_win_condition(self, side, cond):
        self.win_conditions[side].add(cond)
    
    @unbound
    def check_conditions(self):
        self.ensure_registration()
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
        winners = [side for side in result if result[side] == 'win']
        if len(result) == len(self.sides):
            if winners:
                self.state = battle.Won(winners)
            else:
                self.state = battle.finished
        elif len(result)+1 == len(self.sides):
            if winners:
                self.state = battle.Won(winners)
            else:
                self.state = battle.Won([side for side in self.sides if not side in result])

@mod_dep(
    SidedCombat,
    WinLoseConditions,
    TurnEntity,
)
@properties(
    keep_dead=True,
    state=battle.notFinished,
    member_living_listeners=list, # TODO: OrderedSet
)
class SimpleField(Entity):
    @unbound
    def _init(self, *args, **kwargs):
        self.keep_dead = kwargs.get('keep_dead', True)
        self.member_living_listeners.append(self.remove_dead)
        for side in args:
            if not side in self.sides:
                self.add_side(side, Side())
        self.on_new_round(self.simple_field_new_round)
        self.on_new_turn(self.simple_field_new_turn)
    
    @unbound
    def spawn(self, side, entity):
        self.ensure_registration()
        self.sides[side].members.append(entity)
        entity.add_mod(Living)
        if entity.living == 'unborn':
            entity.be_born()
        self.reg_entity(entity)
        entity.add_mod(Sided)
        entity.ally_group = side
        entity.add_mod(BattlefieldEntity)
        entity.field = self
    
    @unbound
    def reg_entity(self, entity):
        for listener in self.member_living_listeners:
            entity.add_listener_node('living', listener())
    
    @unbound
    def unreg_entity(self, entity):
        # need to remove listener..
        if entity.living == 'alive':
            entity.living = 'unborn'
    
    @unbound
    def unspawn(self, entity):
        for side in self.sides:
            if entity in self.sides[side].members:
                self.sides[side].members.remove(entity)
    
    @unbound
    def get_enemies(self, side):
        return set(s for s in self.sides.keys() if self.sides[s] != side)
    
    @unbound
    def simple_field_new_round(self):
        self.ensure_registration()
        for side in self.sides:
            for entity in self.sides[side].members:
                try:
                    entity.new_round()
                except AttributeError:
                    pass
    
    @unbound
    def simple_field_new_turn(self):
        self.ensure_registration()
        self.check_conditions()
    
    @unbound
    def finish(self):
        for side in self.sides.values():
            for entity in side.members:
                self.unreg_entity(entity)
    
    @listener
    def remove_dead(self, target, value):
        if value == 'dead':
            if not self.keep_dead:
                self.unspawn(target)
            self.check_conditions()

@mod_dep(SimpleField)
class TwoSideField(Entity):
    @unbound
    def _init(self, keep_dead=True):
        self.keep_dead = keep_dead
        self.add_side('left', Side())
        self.add_side('right', Side())
