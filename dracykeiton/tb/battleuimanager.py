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

"""BattleUIManager - interface connecting UI and Turnman/Battle
"""

from ..compat import *
from .controller import UserController

class BattleUIManager(object):
    """Helper class which can be used to build battle-controlling UI.
    """
    def __init__(self, turnman):
        super(BattleUIManager, self).__init__()
        self.turnman = turnman
        self.selected = None
    
    def end_turn(self):
        """End turn.
        
        This marks player's turn as being over and processes AI turns
        """
        if isinstance(self.active_controller(), UserController):
            self.active_controller().end_turn()
        # finishes user's turn
        self.turnman.planned_actions()
        # process all AI turns
        while not isinstance(self.active_controller(), UserController):
            self.turnman.turn()
        # start user's turn
        self.turnman.turn()
    
    def active_controller(self):
        return self.turnman.next_side()
    
    def clicked(self, side, entity):
        """Process simple click on entity.
        
        Right now, it selects/"heals" player entity and attacks enemy entity
        """
        if self.selected:
            if self.selected is entity:
                self.selected = None
            else:
                if side is self.active_controller().entity:
                    self.heal(entity)
                    self.selected = None
                else:
                    self.attack(entity)
                    self.selected = None
        else:
            if side is self.active_controller().entity:
                self.selected = entity
    
    def attack(self, entity):
        """Attack given entity
        
        Only possible when there's selected entity and it can act.
        """
        if not self.selected:
            return
        action = self.selected.hit(entity)
        if action:
            self.do_action(action)
    
    def heal(self, entity):
        """"Heal" given entity
        
        TODO: more flexible
        """
        if not self.selected:
            return
        action = self.selected.inspire(entity)
        if action:
            self.do_action(action)
    
    def do_action(self, action):
        """Tell turnman that user wants to perform action"""
        self.active_controller().do_action(action)
        self.turnman.planned_actions()
    
    def start(self):
        """Start manager: this simply starts new turn for user right now.
        
        (this can mean allocating AP for example)
        """
        self.turnman.turn()
