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

"""
"""

from ..compat import *
from .entity import Entity
from .proxyentity import ProxyEntity, CachedEntity

class InterpolatingCache(Entity):
    @unbound
    def _init(self, delay=1.0):
        self.req_mod(ProxyEntity)
        self.req_mod(CachedEntity)
        self.dynamic_property('_interpolating_st', None)
    
    @unbound
    def cache_interpolate_float(self, name, f):
        self.proxy_listen(name)
        self.cache_property(name, self.update)
        self.update_cache(name, 'progress', 1)
    
    @unbound
    def update(self, name, old_value, value):
        self.update_cache(name, 'progress', 0)
    
    @unbound
    def tick(self, st):
        if self._interpolating_st is None:
            self._interpolating_st = st
        time = st-self._interpolating_st
        self._interpolating_st = st
        rs = None
        for name in self._property_cache:
            r = self.update_property(name, time)
            rs = rs or r
        return rs
    
    @unbound
    def update_property(self, name, time):
        pr = self.cached(name, 'progress')
        if pr >= 1:
            self._interpolating_st = None
            return None
        pr = min(1, pr+time)
        self.update_cache(name, 'progress', pr)
        self.update_cache(name, 'current', self.cached(name, 'old')*(1-pr)+self.cached(name, 'new')*pr)
        self.notify_listeners(name)
        return True
