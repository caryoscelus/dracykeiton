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
from ..entity import Entity
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
        self.clear()
    
    def accept(self, entity):
        return False
    
    def ready(self):
        return False
    
    def get(self):
        return None
    
    def clear(self):
        pass

class SingleEnemyAction(UIAction):
    def accept(self, entity):
        if not entity.is_enemy(self.owner):
            return False
        self.enemy = entity
        return True
    
    def ready(self):
        return not self.enemy is None
    
    def get(self):
        return self.f(self.enemy)
    
    def clear(self):
        self.enemy = None

class SingleAllyAction(UIAction):
    def accept(self, entity):
        if not entity.is_ally(self.owner):
            return False
        self.ally = entity
        return True
    
    def ready(self):
        return not self.ally is None
    
    def get(self):
        return self.f(self.ally)
    
    def clear(self):
        self.ally = None

class UniversalBattleAction(UIAction):
    def clear(self):
        f = self.f
        try:
            f.func
        except AttributeError:
            consume_args = 0
        else:
            consume_args = len(f.args)
            f = f.func
        args = f.arguments[consume_args:]
        if f.__defaults__:
            raise NotImplementedError('default argument value handling is not yet implemented')
        self.args = dict({arg : None for arg in args})
    
    def accept(self, entity):
        try:
            entity.ally_group
        except AttributeError:
            is_sided = False
        else:
            is_sided = True
        kind = None
        if is_sided:
            if entity.is_ally(self.owner):
                kind = 'ally'
            elif entity.is_enemy(self.owner):
                kind = 'enemy'
        if kind is None:
            return False
        matching_args = sorted(list([name for name in self.args if not self.args[name] and name.find(kind) > -1]))
        if not matching_args:
            return False
        arg = matching_args[0]
        self.args[arg] = (entity,)
        return True
    
    def ready(self):
        return not [None for name in self.args if not self.args[name]]
    
    def get(self):
        kwargs = dict({arg:self.args[arg][0] for arg in self.args})
        return self.f(**kwargs)

class BattleUIHints(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('_ui_hints', dict())
    
    @unbound
    def ui_action(self, tp, f):
        """Mark the action as available to UI"""
        if not tp in self._ui_hints:
            self._ui_hints[tp] = list()
        self._ui_hints[tp].append(UniversalBattleAction(self, f))
    
    @unbound
    def ui_hints(self, action_type):
        try:
            return self._ui_hints[action_type]
        except KeyError:
            return []

class BattleUIManager(object):
    """Helper class which can be used to build battle-controlling UI.
    """
    def __init__(self, turnman):
        super(BattleUIManager, self).__init__()
        self.turnman = turnman
        self.deselect()
        self.done = False
        self.post_encounter_hooks = list()
    
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
    
    def can_finish(self):
        return False
    
    def end_encounter(self):
        self.done = True
        for f in self.post_encounter_hooks:
            f()
    
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
        self.selected_action.clear()
    
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
