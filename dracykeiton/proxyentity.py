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
from entity import Entity, simplenode

class ProxyEntity(Entity):
    """Entity which gives values from other entity"""
    @unbound
    def _init(self, source=None):
        self._proxy_source = source
    
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
