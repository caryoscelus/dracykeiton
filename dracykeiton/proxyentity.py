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

""""""

from compat import *
from entity import Entity, simplenode, listener

class ProxyEntity(Entity):
    """Entity which gives values from other entity.
    
    It cannot be used as mod because it overrides __getstate__ and
    __getattr__. Perhaps, this can be fixed, if there would be usecase
    for ProxyEntity as mod.
    """
    @unbound
    def _init(self, source=None):
        if not isinstance(self, ProxyEntity):
            raise TypeError('ProxyEntity cannot be used as mod')
        if source or not '_proxy_source' in self.__dict__:
            self._proxy_source = source
    
    def __getstate__(self):
        # clean proxy properties
        self_copy = super(ProxyEntity, self).__getstate__()
        for name in self._proxy_source._props:
            if name in self._props:
                del self_copy['_props'][name]
        return self_copy
    
    def __getattr__(self, name):
        try:
            return super(ProxyEntity, self).__getattr__(name)
        except AttributeError:
            self.proxy_property(name)
            return super(ProxyEntity, self).__getattr__(name)
    
    def proxy_property(self, name):
        if name[:2] == '__':
            return
        self.dynamic_property(name)
        self.add_get_node(name, self.read_source(name))
    
    def read_source(self, name):
        def f(value):
            return getattr(self._proxy_source, name)
        return simplenode(f)()
    
    @unbound
    def proxy_listen(self, name):
        self._proxy_source.add_listener_node(name, self.source_changed(name))
    
    @unbound
    def source_changed(self, name):
        def f(target, value):
            self.notify_listeners(name)
        return listener(f)()

class CachedEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('_propeprty_cache', dict())
    
    @unbound
    def cache_property(self, name, update_f):
        value = getattr(self, name)
        self._proxy_source.add_listener_node(name, self.cache_listener(name, update_f))
        self._propeprty_cache[name] = dict({'new':value, 'old':value, 'current':value})
        self.add_get_node(name, self.get_cache(name))
    
    @unbound
    def get_cache(self, name):
        def f(value):
            return self._propeprty_cache[name]['current']
        return simplenode(f)()
    
    @unbound
    def cache_listener(self, name, update_f):
        def f(target, value):
            old_value = self.cached(name, 'new')
            self.update_cache(name, 'new', value)
            self.update_cache(name, 'old', old_value)
            update_f(name, old_value, value)
        return listener(f)()
    
    @unbound
    def cached(self, name, version):
        return self._propeprty_cache[name][version]
    
    @unbound
    def update_cache(self, name, n, value):
        self._propeprty_cache[name][n] = value
