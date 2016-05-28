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

"""Grid, usually for battlefield

TODO: split & clean this mess
"""

from ..compat import *
from ..entity import Entity, simplenode, depends, mod_dep, properties, listener
from ..action import action
from ..containers import dMultiArray
from .xy import XY
from .ap import ActionPoint
from .battlefield import SimpleField, BattlefieldEntity, Sided

@mod_dep(XY)
@properties(content=dict)
class GridCell(Entity):
    @unbound
    def _init(self, x=None, y=None):
        self.x, self.y = x, y
    
    @unbound
    def get(self, layer=None):
        return self.content.get(layer)

@mod_dep(XY)
@properties(layer=None)
class GridEntity(Entity):
    @unbound
    def _init(self, x=None, y=None, layer=None):
        self.x, self.y = x, y
        self.layer = layer

@mod_dep(SimpleField)
@properties(grid=dMultiArray(2), size=(0, 0))
class GridField(Entity):
    @unbound
    def _init(self, size=None):
        self.grid.empty = lambda coords: GridCell(x=coords[0], y=coords[1])
        if size:
            self.set_size(*size)
        self.member_living_listeners.append(self.remove_dead_from_grid)
    
    @unbound
    def set_size(self, w, h):
        self.grid.set_maxs(w-1, h-1)
        self.size = (w, h)
    
    @unbound
    def put_on(self, x, y, entity, layer=None):
        target_cell = self.grid[x, y]
        if target_cell.content.get(layer, None):
            return
        if not entity.has_mod(GridEntity):
            entity.add_mod(GridEntity, x, y, layer)
        else:
            x0, y0 = entity.x, entity.y
            layer0 = entity.layer
            if x0 == x and y0 == y and layer0 == layer:
                return
            else:
                self.remove_from(x0, y0, layer0)
        target_cell.content[layer] = entity
        entity.x = x
        entity.y = y
    
    @unbound
    def remove_from(self, x, y, layer=None):
        if not (x is None) and not (y is None):
            self.grid[(x, y)].content[layer] = None
    
    @listener
    def remove_dead_from_grid(self, target, value):
        print('remove_dead_from_grid')
        if value == 'dead':
            if not self.keep_dead:
                self.remove_from(target.x, target.y, target.layer)

@mod_dep(GridField)
class FieldRange(Entity):
    @unbound
    def get_range(self, axy, bxy):
        return abs(axy[0]-bxy[0])+abs(axy[1]-bxy[1])

@mod_dep(BattlefieldEntity, GridEntity, Sided)
class ExamineFieldEntity(Entity):
    @unbound
    def get_closest_enemy(self):
        enemy_sides = [
            side
                for (name, side) in self.field.sides.items()
                    if name != self.ally_group
        ]
        enemies = [
            enemy
                for side in enemy_sides
                    for enemy in side.members
        ]
        if not enemies:
            return None
        enemies.sort(
            key=lambda enemy:
                self.field.get_range(self.xy(), enemy.xy())
        )
        return enemies[0]

@mod_dep(ActionPoint, GridEntity, BattlefieldEntity)
class Movable(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('move_constraints', list())
    
    @unbound
    def add_move_constraint(self, constraint):
        self.move_constraints.append(constraint)
    
    @action
    def move(self, x, y):
        self.field.put_on(x, y, self)
    
    @unbound
    def can_move(self, x, y):
        if not all([constraint(x, y) for constraint in self.move_constraints]):
            return False
        return self.spend_ap(1)
