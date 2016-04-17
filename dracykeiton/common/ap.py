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

"""Action point system and stuff related to acting entities in general."""

from ..entity import Entity, simplenode, depends, mod_dep, properties
from .hp import Living
from .turn import TurnEntity
from ..compat import *
from ..util import curry

@properties(can_act=True)
class Acting(Entity):
    """Basic acting entity, only defines can_act property.
    
    This can be used as basis to various possible acting systems.
    """
    pass

@mod_dep(Acting, Living)
class LivingActing(Entity):
    """Ensure only alive entities can act."""
    @unbound
    def _load(self):
        self.add_get_node('can_act', self.check_if_alive())
    
    @depends('living')
    @simplenode
    def check_if_alive(value, living):
        return living == 'alive' and value

@mod_dep(Acting, TurnEntity)
@properties(ap=0, maxap=0)
class ActionPoint(Entity):
    """AP entity, defining AP and maxAP properties and helper functions."""
    @unbound
    def _init(self, maxap=0):
        self.on_turn_end('restore_ap')
        self.maxap = maxap
    
    @unbound
    def spend_ap(self, ap):
        """This can be used by action checker.
        
        Returns True if there was enough AP and it's spent, False otherwise.
        """
        if not self.can_act:
            return False
        if self.ap < ap:
            return False
        else:
            self.ap -= ap
            return True
    
    @unbound
    def restore_ap(self):
        """Mainly to use when new turn starts"""
        self.ap = self.maxap
