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

"""Controller: 
"""

import functools

from compat import *
import curry
from entity import Entity

class ControllableEntity(Entity):
    def __init__(self):
        super(ControllableEntity, self).__init__()
        self.dynamic_property('available_actions', empty=set())

class WorldEntity(Entity):
    def observe(self, observer):
        return self

class Controller(object):
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
    """Controller which is controlled from outside"""
    def __init__(self, *args, **kwargs):
        super(ProxyController, self).__init__(*args, **kwargs)
        self._end_turn = False
        self._next_action = None
    
    def end_turn(self):
        self._end_turn = True
    
    def do_action(self, action):
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

def action(f):
    """Decorator making callable which checks if action is possible.
    
    If it's possible, return curry, else return None. Checker method
    should have same name prefixed with can_
    
    >>> class Foo(Entity):
    ...     @action
    ...     def bar(self, n):
    ...         print(n)
    ...     def can_bar(self, n):
    ...         return n > 0
    >>> foo = Foo()
    >>> foo.bar(5).__name__
    'bar'
    >>> foo.bar(5)()
    5
    >>> print(foo.bar(0))
    None
    """
    @functools.wraps(f)
    def wrap(self, *args, **kwargs):
        if getattr(self, 'can_{}'.format(f.__name__))(*args, **kwargs):
            return curry.curry(f)(self, *args, **kwargs)
        else:
            return None
    return wrap
