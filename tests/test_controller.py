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

"""tests for controller.py"""

from dracykeiton.util import curry
from dracykeiton.tb.controller import Controller, ControllableEntity, ProxyController

def test_controller():
    entity = ControllableEntity()
    controller = Controller(None, entity)

def test_proxy_controller():
    controller = ProxyController(None, None)
    assert controller.act() == False
    controller.end_turn()
    assert controller.act() == None
    assert controller.act() == False
    class Foo():
        def __init__(self):
            self.t = None
        def foo(self):
            self.t = True
    foo = Foo()
    controller.do_action(foo.foo)
    controller.act()()
    assert foo.t is True
