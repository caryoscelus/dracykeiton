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

"""Console controller: console interface for controller

NOTE: this is for testing purposes only; can be insecure

>>> from entity import Entity
>>> from controller import SimpleAction
>>> e = Entity()
>>> e.dynamic_property('n')
>>> @SimpleAction
... def action(target):
...     target.n = 7
>>> c = ConsoleController()
>>> c.get_action = lambda entity: action
>>> c.add_entity(e)
>>> l = c.act()
Entity {'n': None}
>>> l[0][1].act(l[0][0])
>>> print(e)
Entity {'n': 7}
"""

from controller import Controller

class ConsoleController(Controller):
    def act(self):
        r = []
        for entity in self._entities:
            print(entity)
            action = self.get_action(entity)
            r.append((entity, action))
        return r
    
    def get_action(self, entity):
        return eval(input('Your action: '))
