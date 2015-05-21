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

"""Tests for entity.py"""

import pytest

from compat import *
from entity import Entity, simplenode, ReadOnlyNode, DependencyError, EntityMod

def test_entity_property():
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
            self.add_get_node('foo', self.get3())
        
        @simplenode
        def get3(self, value):
            return 3
    
    foo = Foo()
    assert foo.foo == 3
    with pytest.raises(AttributeError):
        foo.foo = 5

def test_processing_node():
    entity = Entity()
    entity.dynamic_property('abc')
    entity.abc = 4
    class FooNode(ReadOnlyNode):
        def process(self, abc, value):
            return value+abc
    node = FooNode()
    with pytest.raises(TypeError):
        node(entity, 5)
    node.depends('abc')
    assert node(entity, 5) == 9

def test_dependencies():
    entity = Entity()
    entity.dynamic_property('foo')
    entity.dynamic_property('bar')
    class BarNode(ReadOnlyNode):
        def __init__(self):
            super(BarNode, self).__init__()
            self.depends('bar')
        def process(self, bar, value):
            return value
    
    class FooNode(ReadOnlyNode):
        def __init__(self):
            super(FooNode, self).__init__()
            self.depends('foo')
        def process(self, foo, value):
            return value
    
    entity.add_get_node('foo', BarNode())
    with pytest.raises(DependencyError):
        entity.add_get_node('bar', BarNode())

def test_mod():
    class FooMod(EntityMod):
        def enable(self, target):
            target.dynamic_property('n')
            target.add_get_node('n', self.get5())
        
        def disable(self, target):
            target.remove_property('n')
        
        @simplenode
        def get5(self, value):
            return 5
    mod = FooMod()
    entity = Entity()
    entity.add_mod(mod)
    assert entity.n == 5
    entity.remove_mod(mod)
    with pytest.raises(AttributeError):
        entity.n

def test_dynamic_method():
    e = Entity()
    e.dynamic_property('n')
    e.n = 5
    e.dynamic_method('method')
    e.method = lambda self: self.n
    assert e.method() == 5

import math

class LevelEntity(Entity):
    def __init__(self):
        super(LevelEntity, self).__init__()
        self.dynamic_property('level')

class XpEntity(LevelEntity):
    def __init__(self):
        super(XpEntity, self).__init__()
        self.dynamic_property('xp', 0)
        self.no_set('level')
        self.add_get_node('level', self.xp_to_level())
    
    @simplenode
    def xp_to_level(self, value):
        return math.log(self.xp / 100 + 1, 2)

class LivingEntity(Entity):
    def __init__(self):
        super(LivingEntity, self).__init__()
        self.dynamic_property('living')
        self.add_set_node('living', self.ensure_correct())
        self.add_get_node('living', self.default_unborn())
    
    @simplenode
    def ensure_correct(self, value):
        if not value in ('unborn', 'alive', 'dead'):
            raise TypeError('living property cannnot equal "{}"'.format(value))
        return value
    
    @simplenode
    def default_unborn(self, value):
        if value is None:
            return 'unborn'
        return value

class HpEntity(LivingEntity):
    def __init__(self):
        super(HpEntity, self).__init__()
        self.dynamic_property('hp', 0)
        self.dynamic_property('maxhp', 0)
        self.add_get_node('hp', self.hp_cap())
        self.add_set_node('hp', self.check_dying())
    
    @simplenode
    def hp_cap(self, value):
        return min(value, self.maxhp)
    
    @simplenode
    def check_dying(self, value):
        if value <= 0:
            self.living = 'dead'
        return value

class RobustEntity(HpEntity):
    def __init__(self):
        super(RobustEntity, self).__init__()
        self.dynamic_property('robust', 1)
        self.add_get_node('maxhp', self.__robust_hp())
    
    @simplenode
    def __robust_hp(self, value):
        return self.robust * value

class Monster(XpEntity, RobustEntity):
    pass

class HpBooster(object):
    def enable(self, target):
        target.add_get_node('maxhp', self.maxhp_booster(), 'early')
    
    def disable(self, target):
        pass
    
    @simplenode
    def maxhp_booster(self, value):
        return value+1

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
    assert monster.hp == 5
    
    booster = HpBooster()
    booster.enable(monster)
    assert monster.maxhp == 5.5
