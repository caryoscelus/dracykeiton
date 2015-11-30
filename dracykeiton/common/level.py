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

"""Level"""

from ..compat import *
from ..entity import Entity, listener, mod_dep
from ..util import curry

class Level(Entity):
    @unbound
    def _init(self, level=0):
        self.dynamic_property('level', level)

@mod_dep(Level)
class LevelAbility(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('level_hooks', dict())
    
    @unbound
    def _load(self):
        self.add_listener_node('level', self.levelup_listener())
    
    @listener
    def levelup_listener(self, target, value):
        for i in range(int(value)+1):
            if i in self.level_hooks:
                for f in self.level_hooks[i]:
                    f()
                del self.level_hooks[i]
    
    @unbound
    def on_level(self, level, f):
        if not level in self.level_hooks:
            self.level_hooks[level] = list()
        self.level_hooks[level].append(f)
    
    @unbound
    def mod_on_level(self, level, mod, *args, **kwargs):
        self.on_level(level, curry.curry(self.add_mod)(mod, *args, **kwargs))
