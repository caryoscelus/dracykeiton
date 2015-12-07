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

"""Test entity mod dynamic loading & unloading"""

import pytest

from dracykeiton.compat import *
from dracykeiton.entity import Entity, mod_dep, properties, data_node

@properties(n=5)
class Foo(Entity):
    pass

@data_node('get', 'n')
def NPlus1(value):
    return value+1

class Bar(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('m')
    @unbound
    def _uninit(self):
        self.remove_property('m')

@mod_dep(Bar)
class Bar2(Entity):
    pass

class NoInit(Entity):
    @unbound
    def t(self):
        pass

def test_manual_unload():
    entity = Entity()
    entity.add_mod(Bar)
    assert entity.m is None
    entity.del_mod(Bar)
    with pytest.raises(AttributeError):
        entity.m

def test_dependency_unload():
    entity = Bar2()
    entity.add_mod(Bar)
    entity.del_mod(Bar)
    assert entity.m is None

def test_noinit_unload():
    entity = Entity()
    entity.add_mod(NoInit)
    entity.del_mod(NoInit)

def test_unload_node():
    foo = Foo()
    foo.add_mod(NPlus1)
    assert foo.n == 6
    foo.del_mod(NPlus1)
    assert foo.n == 5

def test_unload_properties():
    entity = Entity()
    with pytest.raises(AttributeError):
        entity.n
    entity.add_mod(Foo)
    assert entity.n == 5
    entity.n = 6
    assert entity.n == 6
    entity.del_mod(Foo)
    with pytest.raises(AttributeError):
        entity.n
