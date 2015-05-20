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

from savable import Savable
from entity import Entity

class ControllableEntity(Entity):
    def __init__(self):
        super(ControllableEntity, self).__init__()
        self.dynamic_property('available_actions', empty=set())

class Controller(Savable):
    def __init__(self, *args):
        super(Controller, self).__init__()
        self._entities = set(args)
    
    def add_entity(self, entity):
        self._entities.add(entity)
    
    def remove_entity(self, entity):
        self._entities.remove(entity)
    
    def start_acting(self):
        pass
    
    def act(self):
        return None

class Action(Savable):
    def act(self):
        pass

class SimpleAction(Action):
    def __init__(self, f):
        super(SimpleAction, self).__init__()
        self.f = f
    
    def act(self, *args, **kwargs):
        self.f(*args, **kwargs)

def simpleaction(f):
    """Decorator"""
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        return SimpleAction(functools.partial(f, *args, **kwargs))
    return wrap
