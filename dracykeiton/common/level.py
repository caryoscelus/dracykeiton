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
from ..entity import Entity, listener

class LevelEntity(Entity):
    @unbound
    def _init(self, level=0):
        self.dynamic_property('level', level)

class LevelAbility(Entity):
    @unbound
    def _init(self):
        self.req_mod(LevelEntity)
        self.dynamic_property('level_mods', dict())
        self.add_listener_node('level', self.levelup_listener())
    
    @listener
    def levelup_listener(self, target, value):
        for i in range(int(value)+1):
            if i in self.level_mods:
                for mod in self.level_mods[i]:
                    self.req_mod(mod[0], *mod[1], **mod[2])
                del self.level_mods[i]
    
    @unbound
    def on_level(self, level, mod, *args, **kwargs):
        if not level in self.level_mods:
            self.level_mods[level] = list()
        self.level_mods[level].append((mod, args, kwargs))
