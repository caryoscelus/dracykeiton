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
from ..entity import Entity, simplenode, depends
from .kill import KillingEntity
from .level import LevelEntity

import math

class XpEntity(Entity):
    @unbound
    def _init(self, xp=0):
        self.dynamic_property('xp', xp)

class XpKillingEntity(Entity):
    @unbound
    def _init(self):
        self.req_mod(XpEntity)
        self.req_mod(KillingEntity)
        self.on_kill('gain_xp_from_killing')
    
    @unbound
    def gain_xp_from_killing(self, victim):
        self.xp += (victim.level+1)*10

class XpLevelEntity(Entity):
    @unbound
    def _init(self, xp=0):
        self.req_mod(LevelEntity)
        self.req_mod(XpEntity, xp)
        self.add_set_node('level', self.level_to_xp())
        self.add_get_node('level', self.xp_to_level())
    
    @simplenode
    def level_to_xp(self, value):
        self.xp = ((2 ** value)-1)*100
        return None
    
    @depends('xp')
    @simplenode
    def xp_to_level(self, value, xp):
        return math.log(xp / 100 + 1, 2)
