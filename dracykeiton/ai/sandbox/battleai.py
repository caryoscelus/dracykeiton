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

"""Pretty stupid battle AI"""

from ...compat import *
from ... import random
from ...tb.controller import Controller

class AIBattleController(Controller):
    def act(self):
        side = self.entity
        enemy_sides = self.world.get_enemies(side)
        if not enemy_sides:
            return None
        enemy_side = self.world.sides[random.choice(tuple(enemy_sides))]
        for enemy in enemy_side.members:
            if enemy.living == 'alive':
                break
        if not enemy.living == 'alive':
            return None
        for entity in side.members:
            action = entity.hit(enemy)
            if action:
                return action
        return None
