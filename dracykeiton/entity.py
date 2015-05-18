##
##  Copyright (C) 2015 caryoscelus
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

"""Contains Entity which is the base class for all entities and it's properties
"""

from savable import Savable
from priorityqueue import PriorityQueue

import functools

class DynamicProperty(Savable):
    """Stores dynamic property and modifiers associated with it."""
    def __init__(self, empty=None, priorities=(), default=None):
        self.getters = PriorityQueue(*priorities, default=default)
        self.setters = PriorityQueue(*priorities, default=default)
        self.mod_names = {}
        self._value = empty
    
    def __str__(self):
        return str(self.value)
    
    @property
    def value(self):
        value = self._value
        for mod in self.getters:
            value = mod(value)
        return value
    
    @value.setter
    def value(self, value):
        for mod in self.setters:
            value = mod(value)
        self._value = value
    
    def add_set_mod(self, f, priority=None):
        self.setters.add(f, priority)
    
    def add_get_mod(self, f, priority=None):
        self.getters.add(f, priority)

class Entity(Savable):
    """Base entity, including dynamic property mechanism."""
    def __init__(self):
        super(Entity, self).__init__()
        self._props = {}
        # TODO: fix this
        self._priorities = ('early', 'normal', 'late')
        self._default = 'normal'
    
    def __getattr__(self, name):
        if name in self._props:
            return self._props[name].value
        raise AttributeError('{} has no attribute/property {}'.format(self, name))
    
    def __setattr__(self, name, value):
        if name[0] == '_':
            super(Entity, self).__setattr__(name, value)
        elif name in self._props:
            self._props[name].value = value
        else:
            raise AttributeError('{} has no property {}'.format(self, name))
    
    def dynamic_property(self, name, empty=None):
        """Define new dynamic property called name"""
        self._props[name] = DynamicProperty(empty=empty, priorities=self._priorities, default=self._default)
    
    def no_set(self, prop):
        """Forbid setting prop"""
        self.add_set_mod(prop, no_set_mod(self, prop))
    
    def add_set_mod(self, prop, mod, priority=None):
        """Add setter mod"""
        self._props[prop].add_set_mod(mod, priority)
    
    def add_get_mod(self, prop, mod, priority=None):
        """Add getter mod"""
        self._props[prop].add_get_mod(mod, priority)

def property_mod(f):
    """Decorator for property mod.
    
    >>> @property_mod
    ... def f(a, b, value):
    ...     return value*(a-b)
    ... 
    >>> f(5, b=1)(value=4)
    16
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        def f0(value):
            if kwargs:
                args0 = args
                kwargs0 = {'value' : value}
                kwargs0.update(kwargs)
            else:
                args0 = args + (value,)
                kwargs0 = {}
            return f(*args0, **kwargs0)
        return f0
    return wrapper

@property_mod
def no_set_mod(entity, name, value):
    raise AttributeError('{}: property {} cannot be written'.format(entity, name))
