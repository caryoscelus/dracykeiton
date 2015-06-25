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

from ..compat import *
import copy

class DependencyTree(object):
    def __init__(self):
        super(DependencyTree, self).__init__()
        self._deps = dict()
    
    def __iter__(self):
        deps = copy.deepcopy(self._deps)
        stack = list([None])
        while stack:
            target = stack[-1]
            if not target in deps or not deps[target]:
                stack.pop()
                if not target is None:
                    yield target
            else:
                stack.append(deps[target].pop())
    
    def add_dep(self, target, dep):
        """Add dependecy dep to target
        
        DependencyTree always has implicit root target None, so pass it
        to add first dependency.
        """
        if not target in self._deps:
            self._deps[target] = list()
        self._deps[target].append(dep)
