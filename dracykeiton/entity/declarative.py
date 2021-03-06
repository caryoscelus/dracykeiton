##
##  Copyright (C) 2015-2016 caryoscelus
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

"""Tools to make Entity definitions more declarative

This means more separation between data structures and actual code.
"""

from ..compat import *
from .entity import Entity, depends, simplenode, mod_dep

def compound_entity(*mods):
    """Make empty entity class which only depends on other mods
    """
    @mod_dep(*mods)
    class cl(Entity):
        pass
    return cl

def properties(**props):
    """Decorator on Entity class defining dynamic properties
    
    Property default values can either be persistent values
    (numberes, strings, boolean) or functions creating complex
    values. DO NOT pass complex (i.e. changable) objects there, that
    will result in every instance having same object!
    """
    def decorator(cl):
        old_init = cl.__dict__.get('_init')
        old_uninit = cl.__dict__.get('_uninit')
        @unbound
        def new_init(self, *args, **kwargs):
            for name in props:
                if name in kwargs:
                    value = kwargs[name]
                else:
                    value = props[name]
                    if callable(value):
                        value = value()
                self.dynamic_property(name, value)
            if old_init:
                old_init(self, *args, **kwargs)
        @unbound
        def new_uninit(self):
            for name in props:
                self.remove_property(name)
            if old_uninit:
                old_uninit(self)
        cl._init = new_init
        cl._uninit = new_uninit
        return cl
    return decorator

def data_node(tp, target, deps=(), priority=None):
    """Decorator making simple node Entity mod from node function"""
    def decorator(f):
        node = depends(*deps)(simplenode(f))(None)
        class cl(Entity):
            def __reduce__(self):
                import sys
                return (getattr(sys.modules[f.__module__], f.__name__), ())
            
            @unbound
            def _load(self):
                node_f = {
                    'get' : self.add_get_node,
                    'set' : self.add_set_node,
                }
                node_f[tp](target, node, priority)
            
            @unbound
            def _uninit(self):
                node_f = {
                    'get' : self.del_get_node,
                    'set' : self.del_set_node,
                }
                node_f[tp](target, node)
        cl.__module__ = f.__module__
        cl.__name__ = f.__name__
        try:
            cl.__qualname__ = f.__qualname__
        except AttributeError:
            pass
        return cl
    return decorator
