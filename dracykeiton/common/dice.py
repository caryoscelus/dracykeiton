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
from ..entity import Entity, properties
from ..action import action
from ..util import curry
from .. import random

@properties(
    result = None,
    side_count = 1,
    unsaved = False,
)
class Dice(Entity):
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

def get_dice(want, exactly=None, atleast=1, atmost=None):
    try:
        want[0]
    except TypeError:
        want = (want, want)
    
    if not exactly is None:
        try:
            amount = (exactly[0], exactly[1])
        except TypeError:
            amount = (exactly, exactly)
    elif not atmost is None:
        amount = (0, atmost)
    else:
        amount = (atleast, float('inf'))
    return curry.curry(get_dice_f)(want, amount)

def get_dice_f(want, amount, roll_result):
    r = [dice for dice in roll_result if want[0] <= dice <= want[1]]
    return amount[0] <= len(r) <= amount[1]
