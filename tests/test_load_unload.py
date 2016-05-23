##
##  Copyright (C) 2016 caryoscelus
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

from dracykeiton.compat import *
from dracykeiton.entity import Entity, mod_dep, properties, data_node

class Foo(Entity):
    @unbound
    def foo(self):
        return 'foo'

class Bar(Entity):
    @unbound
    def foo(self):
        return 'bar'

@mod_dep(Foo)
class Foo2(Entity):
    pass

@mod_dep(Foo2)
class Foo3(Entity):
    pass

def test_load_unload():
    foo = Entity()
    foo.add_mod(Foo)
    assert foo.foo() == 'foo'
    foo.del_mod(Foo)
    assert not hasattr(foo, 'foo')
    foo.add_mod(Bar)
    assert foo.foo() == 'bar'

def test_load_unload_leveled():
    foo = Entity()
    foo.add_mod(Foo)
    foo.add_mod(Foo3)
    foo.del_mod(Foo3)
    assert foo.foo() == 'foo'

@properties(foo=1)
class Base(Entity):
    pass

@mod_dep(Base)
@data_node('get', 'foo')
def GetNode(value):
    return 0

def test_unload_node():
    base = Base()
    assert base.foo == 1
    base.add_mod(GetNode)
    assert base.foo == 0
    base.del_mod(GetNode)
    assert base.foo == 1
