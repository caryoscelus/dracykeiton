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

"""Dices & rolling them
"""

from ..compat import *
from ..entity import Entity
from ..action import action
from .. import random

class Dice(Entity):
    @unbound
    def _init(self, side_count=None):
        self.dynamic_property('result')
        self.dynamic_property('side_count', side_count)
        self.dynamic_property('unsaved', False)
    
    @action
    def roll_dice(self):
        self.result = random.randint(1, self.side_count)
        self.unsaved = True
    
    @unbound
    def can_roll_dice(self):
        return not self.unsaved
    
    @unbound
    def read(self):
        """Read dice roll. This must be called before next roll."""
        self.unsaved = False
        return self.result
