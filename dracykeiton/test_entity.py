##
##  Copyright (C) 2015 caryoscelus
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

"""Tests for entity.py"""

import pytest

from entity import Entity, property_mod

def test_base_entity():
    entity = Entity()
    entity.dynamic_property('n')
    assert entity.n is None
    entity.n = 5
    assert entity.n is 5

def test_entity_subclass():
    class Foo(Entity):
        def __init__(self):
            super(Foo, self).__init__()
            self.dynamic_property('foo')
            self.no_set('foo')
            self.add_get_mod('foo', self.get3())
            self.dynamic_property('bar')
            self.add_get_mod('bar', self.get4())
        
        def get3(self):
            def g(value):
                return 3
            return g
        
        @property_mod
        def get4(self, value):
            return 4
    
    foo = Foo()
    assert foo.foo == 3
    foo.bar = 5
    assert foo.bar == 4
    assert foo.bar == 4
    with pytest.raises(AttributeError):
        foo.foo = 5


import math

class LevelEntity(Entity):
    def __init__(self):
        super(LevelEntity, self).__init__()
        self.dynamic_property('level')

class XpEntity(LevelEntity):
    def __init__(self):
        super(XpEntity, self).__init__()
        self.dynamic_property('xp')
        self.no_set('level')
        self.add_get_mod('level', self.xp_to_level())
    
    @property_mod
    def xp_to_level(self, value):
        return math.log(self.xp / 100 + 1, 2)

class LivingEntity(Entity):
    def __init__(self):
        super(LivingEntity, self).__init__()
        self.dynamic_property('living')
        self.add_set_mod('living', self.ensure_correct())
        self.add_get_mod('living', self.default_unborn())
    
    @property_mod
    def ensure_correct(self, value):
        if not value in ('unborn', 'alive', 'dead'):
            raise TypeError('living property cannnot equal "{}"'.format(value))
        return value
    
    @property_mod
    def default_unborn(self, value):
        if value is None:
            return 'unborn'
        return value

class HpEntity(LivingEntity):
    def __init__(self):
        super(HpEntity, self).__init__()
        self.dynamic_property('hp')
        self.dynamic_property('maxhp')
        self.add_set_mod('hp', self.hp_cap())
        self.add_set_mod('hp', self.check_dying())
    
    @property_mod
    def hp_cap(self, value):
        return min(value, self.maxhp)
    
    @property_mod
    def check_dying(self, value):
        if value <= 0:
            self.living = 'dead'
        return value

class RobustEntity(HpEntity):
    def __init__(self):
        super(RobustEntity, self).__init__()
        self.dynamic_property('robust', 1)
        self.add_get_mod('maxhp', self.__robust_hp())
    
    @property_mod
    def __robust_hp(self, value):
        return self.robust * value

class Monster(XpEntity, RobustEntity):
    pass

def test_entity_monster():
    monster = Monster()
    monster.xp = 0
    assert monster.level == 0
    monster.xp = 100
    assert monster.level == 1
    monster.xp = 700
    assert monster.level == 3
    
    assert monster.living == 'unborn'
    with pytest.raises(TypeError):
        monster.living = False
    
    monster.maxhp = 10
    monster.hp = 12
    assert monster.hp == 10
    monster.hp -= 11
    assert monster.living == 'dead'
    monster.living = 'alive'
    assert monster.living == 'alive'
    monster.hp = 10
    monster.robust = 0.5
    assert monster.maxhp == 5
