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

"""TurnEntity - entity that is involved in turn-based battles
"""

from ..compat import *
from ..entity import Entity

class TurnEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('turn_hooks', list())
    
    @unbound
    def on_turn_end(self, f):
        self.turn_hooks.append(f)
    
    @unbound
    def new_round(self):
        for f in self.turn_hooks:
            getattr(self, f)()
