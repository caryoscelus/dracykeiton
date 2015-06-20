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

"""Tests for action.py"""

from dracykeiton.compat import *
from dracykeiton.entity import Entity
from dracykeiton.action import action

class ActionEntity(Entity):
    @action
    def foo(self):
        pass
    
    @unbound
    def can_foo(self):
        return True

def test_action_name():
    a = ActionEntity()
    assert a.foo.__name__ == 'foo'
    b = Entity()
    b.req_mod(ActionEntity)
    #assert b.foo.__name__ == 'foo' # <- doesn't work
    # unfortunatelly we can't fix it :(
    # python creates ugly functools.partial when we call non-class method on instance
    assert b.foo.func.__name__ == 'foo'
