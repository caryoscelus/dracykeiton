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

"""Test declarative Entity definitions"""

from dracykeiton.compat import *
from dracykeiton.entity import Entity, properties, mod_dep

def test_declarative_properties():
    @properties({
        'n' : 5,
        'm' : 4,
    })
    class Foo(Entity):
        def _init(self, m=None):
            if not m is None:
                self.m = m
    assert Foo().n == 5
    assert Foo().m == 4
    assert Foo(7).m == 7

def test_no_init():
    @properties({'n' : None})
    class Foo(Entity):
        pass
    assert Foo().n == None

def test_mod():
    @properties({'n' : 3})
    class Foo(Entity):
        pass
    
    @mod_dep(Foo)
    class Bar(Entity):
        pass
    
    assert Bar().n == 3