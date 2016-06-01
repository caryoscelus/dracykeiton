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

"""TurnEntity - entity that is involved in turn-based battles
"""

from ..compat import *
from ..entity import Entity, properties

@properties(
    turn_hooks=list,
    round_hooks=list,
)
class TurnEntity(Entity):
    """Entity mod allowing multiple handlers to run on turn/round ends"""
    @unbound
    def on_new_turn(self, f):
        self.turn_hooks.append(f)
    
    @unbound
    def on_new_round(self, f):
        self.round_hooks.append(f)
    
    @unbound
    def new_turn(self):
        for f in self.turn_hooks:
            f()
    
    @unbound
    def new_round(self):
        for f in self.round_hooks:
            f()
