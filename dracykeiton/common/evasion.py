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

"""Evasion"""

from ..compat import *
from ..entity import Entity, mod_dep, simplenode, depends, properties
from .dexterity import Dexterity

@properties(evasion=0)
class Evasion(Entity):
    pass

@mod_dep(Evasion, Dexterity)
class DexterityBasedEvasion(Entity):
    @unbound
    def _load(self):
        self.add_get_node('evasion', self.get_evasion())
    
    @depends('dexterity')
    @simplenode
    def get_evasion(value, dexterity):
        return dexterity*0.5
