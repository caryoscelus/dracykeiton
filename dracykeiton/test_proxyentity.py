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

"""Test proxy entity
"""

from compat import *
from entity import Entity
from proxyentity import ProxyEntity

class FooEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('n', 0)

def test_simple_proxy():
    foo = FooEntity()
    proxy = ProxyEntity(foo)
    assert proxy.n == 0
    foo.n = 1
    assert proxy.n == 1
