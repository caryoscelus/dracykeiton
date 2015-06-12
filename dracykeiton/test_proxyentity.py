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
from entity import Entity, simplenode
from proxyentity import ProxyEntity, CachedEntity
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
    pickle = import_pickle()
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
    
    @simplenode
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
    proxy.req_mod(SlideNProxy)
    foo.n = 5
    assert proxy.n == 0
    proxy.step()
    assert proxy.n == 1

class CachedN(Entity):
    @unbound
    def _init(self):
        self.req_mod(ProxyEntity)
        self.req_mod(CachedEntity)
        self.proxy_listen('n')
        self.cache_property('n', self.update)
        self.update_cache('n', 'progress', 1)
    
    @unbound
    def update(self, prop, old_value, value):
        self.update_cache(prop, 'progress', 0)
    
    @unbound
    def tick(self, time):
        pr = self.cached('n', 'progress')
        if pr >= 1:
            return
        pr = min(1, pr+time)
        self.update_cache('n', 'progress', pr)
        self.update_cache('n', 'current', self.cached('n', 'old')*(1-pr)+self.cached('n', 'new')*pr)

def test_cached_proxy():
    foo = FooEntity()
    proxy = ProxyEntity(foo)
    proxy.req_mod(CachedN)
    foo.n = 0
    foo.n = 1
    assert proxy.n == 0
    proxy.tick(0.5)
    assert proxy.n == 0.5
    proxy.tick(0.6)
    assert proxy.n == 1

class ProxyFoo(Entity):
    @unbound
    def _init(self):
        self.req_mod(ProxyEntity)

def test_proxy_instance():
    with pytest.raises(TypeError):
        ProxyFoo()
    a = ProxyEntity()
    a.req_mod(ProxyFoo)
