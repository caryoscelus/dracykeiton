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

"""Test whether pickling is working correct for our classes"""

from dracykeiton.compat import *
from dracykeiton.entity import DynamicProperty, simplenode, Entity
from dracykeiton import pickle

def test_pickle_property():
    p = DynamicProperty(empty=0)
    s = pickle.dumps(p)
    p1 = pickle.loads(s)
    assert p1.value == 0
    p = DynamicProperty(empty=0)
    def node(value):
        return value+1
    p.add_get_node(node)
    s = pickle.dumps(p)
    p1 = pickle.loads(s)
    assert p.value == 1
    assert p1.value == 0
    assert p._value == p1._value

class FooEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('n', 5)
    
    @unbound
    def _load(self):
        self.add_get_node('n', self.get1())
    
    @simplenode
    def get1(value):
        return value+1

def test_pickle_entity():
    entity = FooEntity()
    s = pickle.dumps(entity)
    entity1 = pickle.loads(s)
    assert entity.n == 6
    assert entity1.n == 6

def test_mod_entity():
    entity = Entity()
    entity.req_mod(FooEntity)
    entity1 = pickle.loads(pickle.dumps(entity))
    assert entity.n == entity1.n
    entity.n = 6
    assert entity.n == 7
    entity1 = pickle.loads(pickle.dumps(entity))
    assert entity.n == entity1.n
