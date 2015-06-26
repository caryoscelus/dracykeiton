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

"""Xp, level"""

from ..compat import *
from ..entity import Entity, simplenode, writernode, depends, mod_dep
from .kill import KillingEntity
from .level import LevelEntity

import math

class XpEntity(Entity):
    @unbound
    def _init(self, xp=0):
        self.dynamic_property('xp', xp)

@mod_dep(XpEntity, KillingEntity)
class XpKillingEntity(Entity):
    @unbound
    def _init(self):
        self.on_kill('gain_xp_from_killing')
    
    @unbound
    def gain_xp_from_killing(self, victim):
        self.xp += (victim.level+1)*10

@mod_dep(LevelEntity, XpEntity)
class XpLevelEntity(Entity):
    @unbound
    def _init(self):
        pass
    
    @unbound
    def _load(self):
        self.add_set_node('level', self.level_to_xp())
        self.add_get_node('level', self.xp_to_level())
    
    @writernode
    def level_to_xp(self, value):
        self.xp = ((2 ** value)-1)*100
        return 0
    
    @depends('xp')
    @simplenode
    def xp_to_level(value, xp):
        return int(math.log(xp / 100 + 1, 2))
