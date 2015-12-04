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

from ..compat import *
from ..entity import Entity, simplenode, depends, mod_dep
from ..action import action
from .ap import ActionPoint
from .battlefield import GridEntity, BattlefieldEntity

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
