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
from ..entity import Entity, simplenode

import math

class LevelEntity(Entity):
    @unbound
    def _init(self, level=0):
        self.dynamic_property('level', level)

class XpEntity(Entity):
    @unbound
    def _init(self, xp=0):
        self.req_mod(LevelEntity)
        self.dynamic_property('xp', xp)
        self.add_set_node('level', self.level_to_xp())
        self.add_get_node('level', self.xp_to_level())
    
    @simplenode
    def level_to_xp(self, value):
        self.xp = ((2 ** value)-1)*100
        return None
    
    @simplenode
    def xp_to_level(self, value):
        return math.log(self.xp / 100 + 1, 2)
