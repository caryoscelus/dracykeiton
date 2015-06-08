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

"""Test additional effects happening when action occur."""

from compat import *
from entity import Entity
from action import action, ActionProcessor

class FooEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('n', 0)
    
    @action
    def action(self):
        self.n += 1
    
    @unbound
    def can_action(self):
        return True

class Effector(object):
    def __init__(self):
        self.e = 0
    def effect(self):
        self.e += 1

class Processor(ActionProcessor):
    def __init__(self):
        self._effects = dict()
    def process(self, a):
        a()
        if a.__name__ in self._effects:
            self._effects[a.__name__]()
    def add_effect(self, target, effect):
        self._effects[target] = effect

def test_effect():
    entity = FooEntity()
    effector = Effector()
    processor = Processor()
    processor.add_effect('action', effector.effect)
    processor.process(entity.action())
    assert entity.n == 1
    assert effector.e == 1
