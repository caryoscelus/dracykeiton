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
        return False
