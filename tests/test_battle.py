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

from dracykeiton.compat import *

from dracykeiton.entity import Entity, listener
from dracykeiton.tb.controller import Controller, UserController
from dracykeiton.tb.turnman import Turnman
from dracykeiton.ui.battleuimanager import BattleUIManager, SingleEnemyAction, SingleAllyAction
from dracykeiton.action import SimpleEffectProcessor
from dracykeiton.tb.battlegen import BattleGen
from dracykeiton.common.sandbox.goblin import Goblin, GoblinLeader
from dracykeiton.ai.sandbox.battleai import AIBattleController

def prepare_battle(left_c, right_c, turnman, keep_dead=False):
    """Prepare battle with given side controllers"""
    encounter = BattleGen(turnman, keep_dead=keep_dead)
    encounter.add_side('left', left_c, 2, predefined=[Goblin(), GoblinLeader()])
    encounter.add_side('right', right_c, 3, predefined=[Goblin(), Goblin(), Goblin()])
    return encounter.generate()

def test_battle():
    turnman = prepare_battle(AIBattleController, AIBattleController, Turnman)
    turnman.turn()
    left_side = turnman.world.sides['left'].members
    assert left_side[0].ap == 0
    right_side = turnman.world.sides['right'].members
    assert len(right_side) == 1
    turnman.turn()
    assert len(left_side) == 1

def test_inspire():
    turnman = prepare_battle(UserController, AIBattleController, Turnman)
    user_controller = turnman.sides[0]
    enemy_controller = turnman.sides[1]
    user_side = user_controller.entity
    enemy_side = enemy_controller.entity
    goblin = user_side.members[0]
    goblin_leader = user_side.members[1]
    enemy = enemy_side.members[0]
    turnman.turn()
    user_controller.do_action(goblin_leader.inspire(goblin))
    turnman.step(user_controller)
    assert goblin.hit_damage == 6
    user_controller.do_action(goblin.hit(enemy))
    turnman.step(user_controller)
    assert enemy.living == 'dead'

class EffectTurnman(Turnman, SimpleEffectProcessor):
    def __init__(self, *args, **kwargs):
        super(EffectTurnman, self).__init__(*args, **kwargs)
        self.add_effect('hit', self.hit_effect)
        self.hit_number = 0
    
    def hit_effect(self, action):
        assert action.__name__ == 'hit'
        self.hit_number += 1

def test_battle_pickle():
    from dracykeiton import pickle
    turnman = prepare_battle(AIBattleController, AIBattleController, EffectTurnman)
    s = pickle.dumps(turnman)
    goblin = turnman.world.sides['left'].members[0]
    assert len(goblin._listeners['living']) == 2
    turnman1 = pickle.loads(s)
    goblin1 = turnman1.world.sides['left'].members[0]
    assert len(turnman1.world.sides) == 2
    # this should happen automatically at some point..
    # unfortunatelly, there's no guarantee that it will now
    turnman1.world.ensure_registration()
    assert len(goblin1._listeners['living']) == len(goblin._listeners['living'])
    
    turnman1.turn()
    turnman.turn()
    assert len(turnman.world.sides['right'].members) == len(turnman1.world.sides['right'].members)

def test_battle_ui_manager():
    turnman = prepare_battle(UserController, AIBattleController, Turnman)
    manager = BattleUIManager(turnman)
    user_controller = turnman.sides[0]
    enemy_controller = turnman.sides[1]
    user_side = user_controller.entity
    enemy_side = enemy_controller.entity
    goblin0 = user_side.members[0]
    goblin1 = user_side.members[1]
    enemy0 = enemy_side.members[0]
    enemy1 = enemy_side.members[1]
    enemy2 = enemy_side.members[2]
    manager.start()
    assert manager.selected == None
    assert goblin0.ap == 4
    manager.clicked(user_side, goblin0)
    assert manager.selected == goblin0
    manager.select_action(SingleEnemyAction(goblin0, goblin0.hit))
    manager.clicked(enemy_side, enemy0)
    assert enemy0.hp == 2
    manager.select_action(SingleEnemyAction(goblin0, goblin0.hit))
    manager.clicked(enemy_side, enemy0)
    assert enemy0.hp == -1
    assert goblin0.xp == 10
    manager.clicked(user_side, goblin1)
    manager.select_action(SingleEnemyAction(goblin1, goblin1.hit))
    manager.clicked(enemy_side, enemy1)
    manager.clicked(enemy_side, enemy1)
    assert enemy1.hp == -1
    manager.end_turn()
    assert goblin0.hp == -1
    manager.clicked(user_side, goblin1)
    assert goblin1.ap == 4
    manager.clicked(enemy_side, enemy2)
    assert enemy2.hp == 2
    assert goblin1.ap == 2
    manager.clicked(user_side, goblin1)
    manager.clicked(enemy_side, enemy2)
    assert goblin1.ap == 0
    manager.clicked(user_side, goblin1)
    manager.clicked(enemy_side, enemy2)
    assert enemy2.hp == -1

def test_callback_pickle():
    from dracykeiton import pickle
    goblin0 = Goblin()
    enemy0 = Goblin()
    goblin0.restore_ap()
    goblin0.be_born()
    enemy0.be_born()
    container = [goblin0, enemy0]
    reloaded = pickle.loads(pickle.dumps(container))
    goblin1 = reloaded[0]
    enemy1 = reloaded[1]
    
    goblin0.hit(enemy0)()
    goblin0.hit(enemy0)()
    assert enemy0.living == 'dead'
    assert goblin0.xp == 10
    
    goblin1.hit(enemy1)()
    goblin1.hit(enemy1)()
    assert enemy1.living == 'dead'
    assert goblin1.xp == 10
    
    reloaded = pickle.loads(pickle.dumps(container))
    goblin2 = reloaded[0]
    enemy2 = reloaded[1]
    assert enemy2.living == 'dead'
    assert goblin2.xp == 10
