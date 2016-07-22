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

"""Test declarative Entity definitions"""

from dracykeiton.compat import *
from dracykeiton.entity import Entity, properties, mod_dep, data_node, compound_entity

def test_declarative_properties():
    @properties(
        n = 5,
        m = 4,
    )
    class Foo(Entity):
        pass
    assert Foo().n == 5
    assert Foo().m == 4
    assert Foo(m=7).m == 7

def test_declarative_init():
    @properties(t=4)
    class Foo(Entity):
        pass
    assert Foo().t == 4
    assert Foo(t=6).t == 6

def test_no_init():
    @properties(n=None)
    class Foo(Entity):
        pass
    assert Foo().n == None

def test_mod():
    @properties(n=3)
    class Foo(Entity):
        pass
    
    @mod_dep(Foo)
    class Bar(Entity):
        pass
    
    assert Bar().n == 3

def test_mod_dep_order():
    @properties(order=list)
    class Base(Entity):
        pass
    
    @mod_dep(Base)
    class Foo(Entity):
        @unbound
        def _init(self):
            self.order.append('Foo')
    
    @mod_dep(Base)
    class Bar(Entity):
        @unbound
        def _init(self):
            self.order.append('Bar')
    
    @mod_dep(Foo, Bar)
    class FooBar(Entity):
        pass
    
    @mod_dep(Bar, Foo)
    class BarFoo(Entity):
        pass
    
    foobar = FooBar()
    assert foobar.order == ['Foo', 'Bar']
    barfoo = BarFoo()
    assert barfoo.order == ['Bar', 'Foo']

def test_declarative_nodes():
    @properties(n=5, m=1)
    class Foo(Entity):
        pass
    
    @mod_dep(Foo)
    @data_node('get', 'n', deps=('m',))
    def NPlusM(value, m):
        return value+m
    
    @mod_dep(Foo, NPlusM)
    class Bar(Entity):
        pass
    
    bar = Bar()
    assert bar.n == 6
    bar.m = 2
    assert bar.n == 7
    bar.n = 0
    assert bar.n == 2

def test_declarative_lists():
    @properties(lst=list)
    class Foo(Entity):
        pass
    
    foo0 = Foo()
    foo1 = Foo()
    assert not foo0.lst is foo1.lst

def test_compound_entity():
    @properties(a=1)
    class Foo(Entity):
        pass
    @properties(b=4)
    class Bar(Entity):
        pass
    Compound = compound_entity(Foo, Bar)
    compound = Compound()
    assert compound.a == 1
    assert compound.b == 4

@properties(n=13)
class Foo(Entity):
    pass

@mod_dep(Foo)
@data_node('get', 'n')
def Bar(value):
    return value*2

def test_pickle_properties():
    from dracykeiton import pickle
    foo = Foo()
    foo.n = 1
    foo = pickle.loads(pickle.dumps(foo))
    assert foo.n == 1

def test_pickle_node():
    from dracykeiton import pickle
    foo = Bar()
    print(globals()['Bar'])
    foo = pickle.loads(pickle.dumps(foo))
    assert foo.n == 26
