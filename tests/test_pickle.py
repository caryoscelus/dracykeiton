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

"""Test whether pickling works correctly for our classes"""

from dracykeiton.compat import *
from dracykeiton.entity import DynamicProperty, simplenode, Entity, properties, mod_dep, data_node
from dracykeiton.common.sandbox.goblin import GoblinLeader
from dracykeiton import pickle

def test_pickle_property():
    p = DynamicProperty(None, empty=0)
    s = pickle.dumps(p)
    p1 = pickle.loads(s)
    assert p1.value == 0
    p = DynamicProperty(None, empty=0)
    def node(self, value):
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
    entity.add_mod(FooEntity)
    entity1 = pickle.loads(pickle.dumps(entity))
    assert entity.n == entity1.n
    entity.n = 6
    assert entity.n == 7
    entity1 = pickle.loads(pickle.dumps(entity))
    assert entity.n == entity1.n

def test_goblin():
    leader0 = GoblinLeader()
    assert leader0.has_mod(GoblinLeader)
    leader1 = pickle.loads(pickle.dumps(leader0))
    assert leader1.has_mod(GoblinLeader)
    assert leader1.robust == leader0.robust

@properties(bar=5)
class Bar(Entity):
    @unbound
    def get_bar(self):
        return self.bar

@properties(dependency=None)
class Foo(Entity):
    pass

@mod_dep(Foo)
@properties(foo=1)
@data_node('get', 'foo', deps=['dependency'])
def TheNode(value, dependency):
    return value+dependency.get_bar()

def test_dependent_nodes():
    bar = Bar()
    foo = Foo(dependency=bar)
    foo.add_mod(TheNode)
    foo1 = pickle.loads(pickle.dumps(foo))
    assert foo1.foo == 6
    foo1, bar1 = pickle.loads(pickle.dumps([foo, bar]))
    assert foo1.foo == 6
    bar1, foo1 = pickle.loads(pickle.dumps([bar, foo]))
    assert foo1.foo == 6

@properties(funcs=list)
class StoreFuncs(Entity):
    @unbound
    def _load(self):
        self.funcs.append(self.func)
    
    @unbound
    def func(self):
        return 1

def test_store_funcs():
    entity = StoreFuncs()
    assert entity.funcs[0]() == 1
    entity1 = pickle.loads(pickle.dumps(entity))
    assert entity1.funcs[0]() == 1
