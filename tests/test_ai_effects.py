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

"""Test BattleUIManager AI turns processing when effects are pausing"""

from dracykeiton.compat import *
from dracykeiton.ui.battleuimanager import BattleUIManager
from dracykeiton.tb.turnman import LockableTurnman
from dracykeiton.action import SimpleEffectProcessor
from dracykeiton.tb.controller import UserController
from dracykeiton.tb.battlegen import BattleGen
from dracykeiton.ai.sandbox.battleai import AIBattleController
from dracykeiton.common.sandbox.goblin import Goblin

from test_battle import prepare_battle

import time
import threading

class PausingTurnman(LockableTurnman, SimpleEffectProcessor):
    def init_effects(self):
        super(PausingTurnman, self).init_effects()
        self.count = 0
        self.add_effect('hit', self.hit_effect)
    
    def hit_effect(self, action):
        self.count += 1
        self.lock()
        t = threading.Timer(0.05, self.unlock)
        t.start()

def test_ai_effects():
    encounter = BattleGen(PausingTurnman)
    goblin = Goblin()
    enemy0 = Goblin()
    enemy1 = Goblin()
    goblin.maxhp = 50
    encounter.add_side('left', UserController, 1, predefined=[goblin])
    encounter.add_side('right', AIBattleController, 2, predefined=[enemy0, enemy1])
    turnman = encounter.generate()
    manager = BattleUIManager(turnman)
    manager.start()
    assert goblin.ap == 4
    goblin.ap = 0
    assert goblin.ap == 0
    manager.end_turn()
    assert goblin.ap == 0
    assert turnman.count == 1
    assert goblin.hp == 47
    while turnman._locked > 0:
        time.sleep(0.05)
    assert goblin.hp == 38
    assert goblin.ap == 4
