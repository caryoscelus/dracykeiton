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

""""Real-world" test: jrpg-style two-side battle
"""

import copy
import random

from compat import *

from entity import Entity, listener
from controller import Controller
from turnman import Turnman
from ap import ActionPointEntity
from hp import HpEntity
from hit import HittingEntity
from battlefield import Battlefield, Side

class Goblin(Entity):
    @unbound
    def _init(self):
        self.add_mod(HpEntity, 5)
        self.add_mod(ActionPointEntity, 4)
        self.add_mod(HittingEntity, 3)

class AIBattleController(Controller):
    def act(self):
        for side in self.entities:
            enemy_sides = self.world.get_enemies(side)
            if not enemy_sides:
                continue
            enemy_side = self.world.sides[random.choice(tuple(enemy_sides))]
            if not enemy_side.members:
                continue
            enemy = enemy_side.members[0]
            for entity in side.members:
                action = entity.hit(enemy)
                if action:
                    return action
        return None

def prepare_battle(left_c, right_c):
    """Prepare battle with given side controllers"""
    battlefield = Battlefield()
    left_side = Side()
    right_side = Side()
    battlefield.add_side('left', left_side)
    battlefield.add_side('right', right_side)
    left_controller = left_c(battlefield)
    left_controller.add_entity(left_side)
    right_controller = right_c(battlefield)
    right_controller.add_entity(right_side)
    for i in range(2):
        goblin = Goblin()
        battlefield.spawn('left', goblin)
    for i in range(3):
        goblin = Goblin()
        battlefield.spawn('right', goblin)
    turnman = Turnman(battlefield)
    turnman.add_side(left_controller)
    turnman.add_side(right_controller)
    return turnman

def test_battle():
    turnman = prepare_battle(AIBattleController, AIBattleController)
    turnman.turn()
    right_side = turnman.world.sides['right'].members
    assert len(right_side) == 1
    turnman.turn()
    left_side = turnman.world.sides['left'].members
    assert len(left_side) == 1

def test_battle_pickle():
    import sys
    if sys.version_info.major >= 3:
        import pickle
    else:
        import dill as pickle
    turnman = prepare_battle(AIBattleController, AIBattleController)
    s = pickle.dumps(turnman)
    turnman1 = pickle.loads(s)
    goblin = turnman.world.sides['left'].members[0]
    goblin1 = turnman1.world.sides['left'].members[0]
    assert len(goblin1._listeners['living']) == len(goblin._listeners['living'])
    
    turnman1.turn()
    turnman.turn()
    assert len(turnman.world.sides['right'].members) == len(turnman1.world.sides['right'].members)
