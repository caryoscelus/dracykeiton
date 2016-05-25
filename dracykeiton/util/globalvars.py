##
##  Copyright (C) 2016 caryoscelus
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

"""Functions supporting global vars compatible with Ren'Py saving system."""

from ..compat import *

if HAS_RENPY:
    import renpy
    def get(name):
        return getattr(renpy.store, name)
    def set(name, value):
        return setattr(renpy.store, name, value)
else:
    class O(object):
        pass
    global _content
    _content = O()
    def get(name):
        return getattr(_content, name)
    def set(name, value):
        return setattr(_content, name, value)

class AlmostSingleton(object):
    def __new__(cl, *args, **kwargs):
        self = super(AlmostSingleton, cl).__new__(cl)
        self.__init__(*args, **kwargs)
        try:
            get(cl.instance_name())
        except AttributeError:
            set(cl.instance_name(), self)
        return self
    
    @classmethod
    def instance(cl):
        return get(cl.instance_name())
    
    @classmethod
    def instance_name(cl):
        return cl.__name__+'_instance'
