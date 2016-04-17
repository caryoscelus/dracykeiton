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

"""Test AttributeLevelup"""

from dracykeiton.compat import *
from dracykeiton.entity import Entity, mod_dep
from dracykeiton.common import AttributeLevelup, Accuracy, Evasion

@mod_dep(AttributeLevelup, Accuracy)
class Foo(Entity):
    pass

def test_levelup():
    foo = Foo()
    assert foo.level == 0
    assert foo.accuracy == 0
    assert foo.increase_attribute('accuracy') is None
    foo.level = 1
    assert foo.increase_attribute('accuracy') is None
    foo.add_levelup_attribute('accuracy')
    foo.increase_attribute('accuracy')()
    assert foo.accuracy == 1
    assert foo.increase_attribute('accuracy') is None
