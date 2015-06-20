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

"""Inspire action: allies deal more damage"""

from ..compat import *
from ..entity import Entity
from ..action import action

class InspiringEntity(Entity):
    @unbound
    def _init(self):
        pass
    
    @action
    def inspire(self, ally):
        ally.be_inspired()
    
    @unbound
    def can_inspire(self, ally):
        try:
            ally.inspired
        except AttributeError:
            return False
        if ally.inspired:
            return False
        return self.spend_ap(2)

class InspirableEntity(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('inspired', False)
    
    @unbound
    def be_inspired(self):
        self.inspired = True
