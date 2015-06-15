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

"""Controller: thing that controlls Entity. Can be AI or user or remote..
"""

import functools

from .compat import *
from . import curry
from .entity import Entity

class ControllableEntity(Entity):
    """Entity which can be controlled?
    
    NOTE: is this required?
    """
    def __init__(self):
        super(ControllableEntity, self).__init__()
        self.dynamic_property('available_actions', empty=set())

class WorldEntity(Entity):
    """Perhaps this can be useful for incomplete information games."""
    @unbound
    def observe(self, observer):
        return self

class Controller(object):
    """"""
    def __init__(self, world, *args):
        super(Controller, self).__init__()
        self.entities = set(args)
        self.world = world
    
    def set_world(self, world):
        self.world = world
    
    def add_entity(self, entity):
        self.entities.add(entity)
    
    def remove_entity(self, entity):
        self.entities.remove(entity)
    
    def act(self):
        """Return next action.
        
        Or False if action is not ready or None if turn is over
        """
        return None

class ProxyController(Controller):
    """Controller which is controlled from outside.
    
    Typical usage for this is player's controller which is controlled by UI,
    but other usecases can include remote users and even some kind of AI
    (e.g. running in separate thread)
    """
    def __init__(self, *args, **kwargs):
        super(ProxyController, self).__init__(*args, **kwargs)
        self._end_turn = False
        self._next_action = None
    
    def end_turn(self):
        """Mark current turn as finished"""
        self._end_turn = True
    
    def do_action(self, action):
        """Next time we're asked for an action (through act) we'll return this.
        
        NOTE: currently only one action is stored!
        """
        self._next_action = action
    
    def act(self):
        if self._end_turn:
            self._end_turn = False
            return None
        if self._next_action:
            action = self._next_action
            self._next_action = None
            return action
        return False

class UserController(ProxyController):
    """A proxy controller, marked as UserController for UI systems convenience"""
    pass
