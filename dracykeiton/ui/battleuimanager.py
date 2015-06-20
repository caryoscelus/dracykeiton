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
from ..tb.controller import UserController

class UIAction(object):
    def __init__(self, owner, f):
        super(UIAction, self).__init__()
        self.owner = owner
        self.f = f
        try:
            self.name = f.__name__
        except AttributeError:
            # duh, f is a functools.partial
            # this can happen if f is rebound action
            self.name = f.func.__name__
    
    def accept(self, entity):
        return False
    
    def ready(self):
        return False
    
    def get(self):
        return None

class SingleEnemyAction(UIAction):
    def __init__(self, *args, **kwargs):
        super(SingleEnemyAction, self).__init__(*args, **kwargs)
        self.enemy = None
    
    def accept(self, entity):
        if not entity.is_enemy(self.owner):
            return False
        self.enemy = entity
        return True
    
    def ready(self):
        return not self.enemy is None
    
    def get(self):
        return self.f(self.enemy)

class SingleAllyAction(UIAction):
    def __init__(self, *args, **kwargs):
        super(SingleAllyAction, self).__init__(*args, **kwargs)
        self.ally = None
    
    def accept(self, entity):
        if not entity.is_ally(self.owner):
            return False
        self.ally = entity
        return True
    
    def ready(self):
        return not self.ally is None
    
    def get(self):
        return self.f(self.ally)

class BattleUIManager(object):
    """Helper class which can be used to build battle-controlling UI.
    """
    def __init__(self, turnman):
        super(BattleUIManager, self).__init__()
        self.turnman = turnman
        self.deselect()
    
    def deselect(self):
        self.selected = None
        self.selected_action = None
    
    def start(self):
        """Start manager: this simply starts new turn for user right now.
        
        (this can mean allocating AP for example)
        """
        self.turnman.turn()
    
    def end_turn(self):
        """End turn.
        
        This marks player's turn as being over and processes AI turns
        """
        if isinstance(self.active_controller(), UserController):
            self.active_controller().end_turn()
        # finishes user's turn
        self.turnman.planned_actions()
        # process all AI turns & start player's turn
        while self.turnman.turn() is None:
            pass
    
    def get_actions(self, entity, action_type):
        if entity == self.selected:
            try:
                entity.ui_hints
            except AttributeError:
                # no UIHints provided..
                return []
            else:
                return entity.ui_hints(action_type)
        return []
    
    def select_action(self, action):
        self.selected_action = action
    
    def active_controller(self):
        return self.turnman.next_side()
    
    def clicked(self, side, entity):
        """Process simple click on entity.
        
        Right now, it selects/"heals" player entity and attacks enemy entity
        """
        if self.selected:
            if self.selected is entity:
                self.deselect()
            elif self.selected_action:
                if self.selected_action.accept(entity):
                    if self.selected_action.ready():
                        self.do_action(self.selected_action.get())
        else:
            if side is self.active_controller().entity:
                self.selected = entity
    
    def do_action(self, action):
        """Tell turnman that user wants to perform action"""
        self.active_controller().do_action(action)
        self.turnman.planned_actions()
