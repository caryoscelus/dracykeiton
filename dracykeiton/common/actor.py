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

"""Actor: Entity having a planned action"""

from ..compat import *
from ..entity import Entity, properties, mod_dep, simplenode

@properties(action=None)
class Actor(Entity):
    """Entity with a planned action
    
    Currently only argumentless actions are supported.
    """
    @unbound
    def plan_action(self, action):
        self.action = action

@properties(action_chance=1.0)
@mod_dep(Actor)
class ActionChance(Entity):
    """Actor with actions having chance of succeeding"""
    pass
