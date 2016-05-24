##
##  Copyright (C) 2015-2016 caryoscelus
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

"""Accuracy stat"""

from ..compat import *
from ..entity import Entity, simplenode, depends, mod_dep, properties
from .dexterity import Dexterity
from .. import random

@properties(accuracy=1)
class Accuracy(Entity):
    pass

@mod_dep(Accuracy)
class RandomAccuracy(Entity):
    @unbound
    def _load(self):
        self.add_get_node('accuracy', self.random_accuracy())
    
    @simplenode
    def random_accuracy(value):
        return value*random.random()

@mod_dep(Accuracy, Dexterity)
class DexterityBasedAccuracy(Entity):
    """Accuracy based on dexterity.
    
    Right now it simply returns dexterity as accuracy, unchanged.
    TODO: use some proper formula?
    """
    @unbound
    def _load(self):
        self.add_get_node('accuracy', self.get_accuracy())
    
    @depends('dexterity')
    @simplenode
    def get_accuracy(value, dexterity):
        return dexterity
