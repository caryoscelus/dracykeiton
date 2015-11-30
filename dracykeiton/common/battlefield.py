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
from ..entity import Entity, listener, mod_dep
from ..tb import battle
from .xy import XY

class Sided(Entity):
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

@mod_dep(Sided)
class Side(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('members', [])
    
    @unbound
    def empty_side(self):
        return all([member.living != 'alive' for member in self.members])

class SidedCombat(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('sides', dict())
        self.dynamic_property('to_reg', list())
    
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
        side.add_mod(Sided, name)
        side.ally_group = name
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
                self.state = battle.Finished()
        elif len(result)+1 == len(self.sides):
            if winners:
                self.state = battle.Won(winners)
            else:
                self.state = battle.Won([side for side in self.sides if not side in result])

@mod_dep(SidedCombat, WinLoseConditions)
class SimpleField(Entity):
    @unbound
    def _init(self, *args, **kwargs):
        keep_dead = kwargs.get('keep_dead', True)
        self.dynamic_property('keep_dead', keep_dead)
        self.dynamic_property('state', battle.NotFinished())
        for side in args:
            if not side in self.sides:
                self.add_side(side, Side())
    
    @unbound
    def spawn(self, side, entity):
        self.ensure_registration()
        self.sides[side].members.append(entity)
        if entity.living == 'unborn':
            entity.be_born()
        self.reg_entity(entity)
        entity.add_mod(Sided, side)
        entity.add_mod(BattlefieldEntity)
        entity.field = self
    
    @unbound
    def reg_entity(self, entity):
        entity.add_listener_node('living', self.remove_dead())
    
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
    def new_round(self):
        self.ensure_registration()
        for side in self.sides:
            for entity in self.sides[side].members:
                try:
                    entity.new_round()
                except AttributeError:
                    pass
    
    @unbound
    def new_turn(self):
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

@mod_dep(XY)
class GridCell(Entity):
    @unbound
    def _init(self, x=None, y=None, content=None):
        if not content:
            content = dict()
        self.dynamic_property('content', content)
        self.x = x
        self.y = y
    
    @unbound
    def get(self, layer=None):
        return self.content.get(layer)

@mod_dep(XY)
class GridEntity(Entity):
    @unbound
    def _init(self, x=None, y=None, layer=None):
        self.dynamic_property('layer', layer)

@mod_dep(SimpleField)
class GridField(Entity):
    @unbound
    def _init(self, w=1, h=1):
        self.dynamic_property('grid', None)
        self.dynamic_property('size', None)
        self.init_grid(w, h)
    
    @unbound
    def init_grid(self, w, h):
        self.grid = [[GridCell(x, y) for x in range(w)] for y in range(h)]
        self.size = (w, h)
    
    @unbound
    def put_on(self, x, y, entity, layer=None):
        if not entity.has_mod(GridEntity):
            entity.add_mod(GridEntity, x, y, layer)
        else:
            x0, y0 = entity.x, entity.y
            layer0 = entity.layer
            if x0 == x and y0 == y and layer0 == layer:
                return
            else:
                self.remove_from(x0, y0, layer0)
        self.grid[y][x].content[layer] = entity
        entity.x = x
        entity.y = y
    
    @unbound
    def remove_from(self, x, y, layer=None):
        if not (x is None) and not (y is None):
            self.grid[y][x].content[layer] = None

@mod_dep(SimpleField)
class TwoSideField(Entity):
    @unbound
    def _init(self, keep_dead=True):
        self.keep_dead = keep_dead
        self.add_side('left', Side())
        self.add_side('right', Side())
