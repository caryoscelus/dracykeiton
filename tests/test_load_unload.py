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
from dracykeiton.entity import Entity

class Foo(Entity):
    @unbound
    def foo(self):
        return 'foo'

class Bar(Entity):
    @unbound
    def foo(self):
        return 'bar'

def test_load_unload():
    foo = Entity()
    foo.add_mod(Foo)
    assert foo.foo() == 'foo'
    foo.del_mod(Foo)
    assert not hasattr(foo, 'foo')
    foo.add_mod(Bar)
    assert foo.foo() == 'bar'
