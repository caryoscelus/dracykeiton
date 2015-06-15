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

from .compat import *
from .action import ActionProcessor
import copy

class Turnman(ActionProcessor):
    def __init__(self, world):
        super(Turnman, self).__init__()
        self.queue = list()
        self.world = world
        self.sides = list()
        self.turn_prepared = False
        self._planned = list()
        self._turns_planned = 0
    
    def add_side(self, controller):
        """Add side"""
        self.sides.append(controller)
    
    def next_side(self):
        """Returns next side or None if no sides"""
        if not self.sides:
            return None
        if self.queue:
            return self.queue[0]
        else:
            return self.sides[0]
    
    def new_round(self):
        """Called when new round starts"""
        self.queue = copy.copy(self.sides)
        try:
            self.world.new_round()
        except AttributeError:
            pass
        try:
            self.world.new_turn()
        except AttributeError:
            pass
    
    def new_turn(self):
        """Called when next side's turn begins"""
        self.queue.pop(0)
        try:
            self.world.new_turn()
        except AttributeError:
            pass
    
    def turn(self):
        """Advance till turn ends.
        
        NOTE: if actions required to end turn cannot be performed now, they'll
        be performed as soon as possible (call planned_actions() to try
        perform such delayed actions)
        
        NOTE: should be called only once for a turn. To finish uncompleted turn,
        use planned_actions() instead.
        
        Returns whatever the last step call returned (None if turn is over,
        False if there are still unperformed actions left)
        """
        if self.planned_actions():
            self._turns_planned += 1
            return False
        
        side = self.next_side()
        if side is None:
            return None
        if not self.queue:
            self.new_round()
        
        r = True
        while r:
            r = self.step(side)
        if r is None:
            self.new_turn()
        else:
            self._turns_planned += 1
        return r
    
    def step(self, side):
        """Process one step of given side.
        
        Returns True if action was performed and there are more, False if
        no action could be performed, None if side's turn is finished.
        """
        r = side.act()
        if r:
            # action is present
            ar = self.process(r)
            if not ar:
                self.plan_action(r)
                return False
            return True
        # if not r, r is either False or None
        return r
    
    def plan_action(self, a):
        self._planned.append(a)
    
    def planned_actions(self):
        """Perform all planned actions.
        
        Return True if there are some actions left, False otherwise
        """
        if self._planned:
            ar = True
            while ar and self._planned:
                next_action = self._planned[0]
                ar = self.process(next_action)
                if ar:
                    self._planned.pop(0)
            if not ar:
                return True
        if self._turns_planned > 0:
            self._turns_planned -= 1
            r = self.turn()
            if r is None:
                return False
        return False

class LockableTurnman(Turnman):
    """Turnman that can be locked and then actions are not performed.
    
    This is useful for performing various effects when actions happen.
    """
    def __init__(self, *args, **kwargs):
        super(LockableTurnman, self).__init__(*args, **kwargs)
        self._locked = 0
    
    def lock(self):
        """Add lock."""
        self._locked += 1
    
    def unlock(self):
        """Release lock. This will also perform planned actions if fully unlocked"""
        self._locked -= 1
        if self._locked < 0:
            raise RuntimeError('too much unlocking')
        if self._locked == 0:
            self.planned_actions()
    
    def process(self, a):
        if self._locked > 0:
            return False
        return super(LockableTurnman, self).process(a)
