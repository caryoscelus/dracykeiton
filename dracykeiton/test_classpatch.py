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

"""Test classpatch"""

from compat import *
import classpatch
from entity import Entity

class FooEntity(Entity):
    pass


class PatchEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('n', 5)

class AnotherPatchEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('m', 7)

classpatch.register(FooEntity, 'mod', PatchEntity)

def test_simple():
    entity = FooEntity()
    assert entity.n == 5

def test_pickle():
    import sys
    if sys.version_info.major >= 3:
        import pickle
    else:
        import dill as pickle
    entity = FooEntity()
    classpatch.register(FooEntity, 'mod', AnotherPatchEntity)
    entity1 = pickle.loads(pickle.dumps(entity))
    assert entity1.n == 5
    assert entity1.m == 7
