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
from .controller import UserController

class BattleUIManager(object):
    """Helper class which can be used to build battle-controlling UI.
    
    NOTE: We expect two-side battle with only one side controlled by user!
    NOTE: We also expect that the first turn is user's
    TODO: Make it flexible
    """
    def __init__(self, turnman):
        super(BattleUIManager, self).__init__()
        self.turnman = turnman
        self.selected = None
        self.user_controller = [s for s in self.turnman.sides if isinstance(s, UserController)][0]
    
    def clicked(self, side, entity):
        """Process simple click on entity.
        
        Right now, it selects player entity and attacks enemy entity
        """
        controller = [s for s in self.turnman.sides if s.entity == side][0]
        if isinstance(controller, UserController):
            self.select(entity)
        else:
            self.attack(entity)
    
    def select(self, entity):
        """This selects given entity.
        
        Some (most currently) actions use selected entity.
        """
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
    
    def do_action(self, action):
        """Tell turnman that user wants to perform action"""
        self.user_controller.do_action(action)
        self.turnman.planned_actions()
    
    def start(self):
        """Start manager: this simply starts new turn for user right now.
        
        (this can mean allocating AP for example)
        """
        self.turnman.turn()
    
    def end_turn(self):
        """End turn.
        
        This marks player's turn as being over and starts AI turn (which ends
        automatically if everything is fine and then new player turn begins)
        
        NOTE: this relies on having only two (player and AI) sides.
        """
        self.user_controller.end_turn()
        self.turnman.planned_actions()
        self.turnman.turn()
        self.turnman.turn()
