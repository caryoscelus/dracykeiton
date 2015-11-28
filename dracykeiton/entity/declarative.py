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

"""Tools to make Entity definitions more declarative

This means more separation between data structures and actual code.
"""

from ..compat import *

def properties(props):
    """Decorator on Entity class defining dynamic properties"""
    def decorator(cl):
        old_init = None
        if '_init' in cl.__dict__:
            old_init = cl._init
        def new_init(self, *args, **kwargs):
            for name in props:
                self.dynamic_property(name, props[name])
            if old_init:
                old_init(self, *args, **kwargs)
        cl._init = new_init
        return cl
    return decorator
