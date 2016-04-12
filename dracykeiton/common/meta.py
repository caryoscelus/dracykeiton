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

from ..compat import *
from ..entity import Entity, properties

@properties(name='')
class Name(Entity):
    """Entity with a name"""
    @unbound
    def _init(self, name=''):
        self.name = name

@properties(id='')
class Id(Entity):
    @unbound
    def _init(self, id=''):
        self.id = id

@properties(description='')
class Description(Entity):
    pass

@properties(tags=set)
class Tags(Entity):
    pass
