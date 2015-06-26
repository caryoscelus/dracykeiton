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

def copy2(d):
    """Copy two levels.
    
    Currently takes dict of lists
    """
    return { k:copy.copy(d[k]) for k in d }

class DependencyTree(object):
    def __init__(self, deps=dict()):
        super(DependencyTree, self).__init__()
        self._deps = copy2(deps)
    
    @classmethod
    def collect(cl, root, f):
        """Alternative way to create DependencyTree from existing structures
        
        f should be function which returns list of dependencies when supplied
        with node
        
        root should be first node of tree
        """
        deps = dict()
        stack = list([None])
        nodes = list([root])
        done = set()
        while stack:
            target = stack[-1]
            if not target in deps:
                deps[target] = list()
            for node in nodes:
                deps[target].append(node)
            if not nodes:
                node = stack.pop()
                done.add(node)
                continue
            target = nodes.pop()
            if target in done:
                continue
            else:
                stack.append(target)
                nodes = f(target)
        return DependencyTree(deps)
    
    def __iter__(self):
        deps = copy2(self._deps)
        stack = list([None])
        while stack:
            target = stack[-1]
            if not target in deps or not deps[target]:
                stack.pop()
                if stack:
                    deps[stack[-1]].remove(target)
                if not target is None:
                    yield target
            else:
                if deps[target][-1] in stack:
                    raise DependencyLoopError('DependencyTree has dependency loop')
                stack.append(deps[target][-1])
    
    def add_dep(self, target, dep):
        """Add dependency dep to target
        
        DependencyTree always has implicit root target None, so pass it
        to add first dependency.
        """
        if not target in self._deps:
            self._deps[target] = list()
        self._deps[target].append(dep)

class DependencyLoopError(RuntimeError):
    pass
