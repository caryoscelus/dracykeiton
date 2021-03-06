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

from dracykeiton.compat import *
from dracykeiton.entity import Entity
from dracykeiton.action import action, ActionProcessor, SimpleEffectProcessor

class ActionEntity(Entity):
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
    def effect(self, eff):
        self.e += 1

def test_effect():
    entity = ActionEntity()
    effector = Effector()
    processor = SimpleEffectProcessor()
    processor.add_effect('action', effector.effect)
    processor.process(entity.action())
    assert entity.n == 1
    assert effector.e == 1

class CountingProcessor(SimpleEffectProcessor):
    def __init__(self, *args, **kwargs):
        super(CountingProcessor, self).__init__(*args, **kwargs)
        self.add_effect('action', self.action)
        self.count = 0
    
    def action(self, action):
        assert action.__name__ == 'action'
        self.count += 1

def test_custom_pickle():
    from dracykeiton import pickle
    entity = ActionEntity()
    processor = CountingProcessor()
    processor0 = pickle.loads(pickle.dumps(processor))
    processor0.process(entity.action)
    assert processor0.count == 1
