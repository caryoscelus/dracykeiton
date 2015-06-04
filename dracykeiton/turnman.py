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

""""""

from compat import *

class Turnman(object):
    def __init__(self, world):
        super(Turnman, self).__init__()
        self.queue = []
        self.back_queue = []
        self.world = world
        self.sides = []
        self.turn_prepared = False
    
    def add_side(self, controller):
        self.queue.append(controller)
        self.sides.append(controller)
    
    def turn(self):
        if not self.queue and not self.back_queue:
            raise IndexError('cannot process turn when there are no sides')
        if not self.turn_prepared:
            self.turn_prepared = True
            if not self.queue:
                self.queue = self.back_queue
                self.back_queue = []
                try:
                    self.world.big_turn()
                except AttributeError:
                    pass
            else:
                try:
                    self.world.small_turn()
                except AttributeError:
                    pass
        side = self.queue.pop(0)
        r = side.act()
        if not r:
            self.queue.insert(0, side)
            return False
        self.back_queue.append(side)
        self.turn_prepared = False
        return True

class SimpleSideTurnman(Turnman):
    pass
