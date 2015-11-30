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

from dracykeiton.compat import *
from dracykeiton.entity import Entity, simplenode, writernode
from dracykeiton.entity.proxyentity import ProxyEntity, CachedEntity
from dracykeiton.entity.interpolate import InterpolatingCache
import pytest

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

class ProxyContainer(object):
    def __init__(self):
        self.foo = FooEntity()
        self.proxy = ProxyEntity(self.foo)

def test_proxy_pickle():
    from dracykeiton import pickle
    container = ProxyContainer()
    assert container.proxy.n == 0
    container = pickle.loads(pickle.dumps(container))
    assert container.proxy.n == 0
    container.foo.n = 1
    assert container.proxy.n == 1

class SlideNProxy(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('n_current')
        self.dynamic_property('n_target')
        self.add_get_node('n', self.slide_n())
    
    @writernode
    def slide_n(self, value):
        self.n_target = value
        if self.n_current is None:
            self.n_current = value
        return self.n_current
    
    @unbound
    def step(self):
        if self.n_current is None:
            return
        self.n_current += (lambda a, b: (a > b) - (a < b))(self.n_target, self.n_current)

def test_modded_proxy():
    foo = FooEntity()
    proxy = ProxyEntity(foo)
    assert proxy.n == 0
    proxy.add_mod(SlideNProxy)
    foo.n = 5
    assert proxy.n == 0
    proxy.step()
    assert proxy.n == 1

def linear(t):
    return t

def test_cached_interpolating_proxy():
    foo = FooEntity()
    proxy = ProxyEntity(foo)
    proxy.add_mod(InterpolatingCache)
    proxy.cache_interpolate_float('n', linear)
    foo.n = 0
    foo.n = 1
    proxy.tick(0)
    assert proxy.n == 0
    proxy.tick(0.5)
    assert proxy.n == 0.5
    proxy.tick(1.0)
    assert proxy.n == 1

class ProxyFoo(Entity):
    @unbound
    def _init(self):
        self.add_mod(ProxyEntity)

def test_proxy_instance():
    with pytest.raises(TypeError):
        ProxyFoo()
    a = ProxyEntity()
    a.add_mod(ProxyFoo)

def test_equality():
    entity = Entity()
    proxy0 = ProxyEntity(entity)
    proxy1 = ProxyEntity(entity)
    proxy_other = ProxyEntity(Entity())
    assert proxy0 == proxy1
    assert proxy0 != proxy_other

def test_proxy_graceful_fail():
    with pytest.raises(AttributeError):
        ProxyEntity(Entity()).a

def test_proxy_set():
    a = FooEntity()
    proxy = ProxyEntity(a)
    proxy.n = 5
    assert a.n == 5
