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
from action import ActionProcessor

class Turnman(ActionProcessor):
    def __init__(self, world):
        super(Turnman, self).__init__()
        self.queue = []
        self.back_queue = []
        self.world = world
        self.sides = []
        self.turn_prepared = False
        self._planned = []
    
    def add_side(self, controller):
        self.queue.append(controller)
        self.sides.append(controller)
    
    def start(self):
        try:
            self.world.big_turn()
            self.turn_prepared = True
        except AttributeError:
            pass
    
    def turn(self):
        r = False
        while r == False:
            r = self.step()
        return r
    
    def plan_action(self, a):
        self._planned.append(a)
    
    def step(self):
        if self._planned:
            ar = True
            while ar and self._planned:
                next_action = self._planned[0]
                ar = self.process(next_action)
                if ar:
                    self._planned.pop(0)
            if not ar:
                return
        
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
        if r:
            # action is present
            ar = self.process(r)
            if not ar:
                self.plan_action(r)
        if not r is None:
            # either action or idle, but anyway, turn is not over yet
            self.queue.insert(0, side)
            if r:
                return False
            else:
                return None
        self.back_queue.append(side)
        self.turn_prepared = False
        return True

class LockableTurnman(Turnman):
    def __init__(self, *args, **kwargs):
        super(LockableTurnman, self).__init__(*args, **kwargs)
        self._locked = 0
    
    def lock(self):
        self._locked += 1
    
    def unlock(self):
        self._locked -= 1
        if self._locked < 0:
            raise RuntimeError('too much unlocking')
    
    def process(self, a):
        if self._locked > 0:
            return False
        return super(LockableTurnman, self).process(a)
