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

"""Compatibility layer.

If Ren'Py is present, import some standard types/functions from renpy.store.

If python2, define unbinding helper methods, else they are empty.
"""

from __future__ import print_function

# currently disabled because harms loading..
_enable_rollback = False

try:
    import renpy as _renpy
    if _enable_rollback:
        from renpy.store import object, list, dict, set, range, sorted
    HAS_RENPY = True
except ImportError:
    HAS_RENPY = False

import sys
if sys.version_info.major < 3:
    import functools
    import collections
    class unbound(object):
        def __init__(self, f):
            self.f = f
            functools.update_wrapper(self, f)
        def __call__(self, *args, **kwargs):
            return self.f(*args, **kwargs)

    def fix_methods(self):
        for name in dir(self):
            method = getattr(self, name)
            if isinstance(method, unbound):
                setattr(self, name, functools.partial(method, self))
    
    if HAS_RENPY:
        import dill
else:
    def unbound(f):
        return f
    def fix_methods(self):
        pass
