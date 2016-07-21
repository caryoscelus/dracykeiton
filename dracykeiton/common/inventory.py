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

"""Inventory"""

from ..compat import *
from ..entity import Entity, properties, mod_dep

@properties(inv=list)
class SimpleInventory(Entity):
    @unbound
    def put_to_inv(self, thing):
        self.inv.append(thing)
    
    @unbound
    def take_from_inv(self, thing):
        if thing in self.inv:
            self.inv.remove(thing)
            return thing
        return None

@properties(equip_slots=list)
class Equip(Entity):
    """Base class for equip using simple slot model.
    
    Create equip slot subclasses with equip_slot function.
    """
    pass

def equip_slot(name):
    """Creates entity mod which adds named equip slot.
    """
    @mod_dep(Equip)
    @properties(**{name:None})
    class cl(Entity):
        @unbound
        def _init(self):
            if name not in self.equip_slots:
                self.equip_slots.append(name)
    return cl

Wield = equip_slot('wielded')
