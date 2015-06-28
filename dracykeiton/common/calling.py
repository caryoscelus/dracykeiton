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
from ..entity import Entity, simplenode, mod_dep
from ..action import action
from .ap import ActionPoint
from .battlefield import BattlefieldEntity

@mod_dep(ActionPoint, BattlefieldEntity)
class Caller(Entity):
    @unbound
    def _init(self, calling_type=None):
        self.dynamic_property('calling_type', calling_type)
    
    @action
    def call_unit(self):
        unit = self.calling_type()
        self.field.spawn(self.ally_group, unit)
    
    @unbound
    def can_call_unit(self):
        return self.spend_ap(4)
