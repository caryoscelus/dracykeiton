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

""""""

from compat import *
from controller import Controller
from turnman import Turnman
from entity import Entity

def test_turnman():
    turnman = Turnman(None)
    player = Controller(None)
    enemy = Controller(None)
    turnman.add_side(player)
    turnman.add_side(enemy)
    turnman.turn()
    player_c = Entity()
    enemy_c = Entity()
    player.add_entity(player_c)
    enemy.add_entity(enemy_c)

def test_pickle():
    import pickle
    from sys import version_info
    if version_info.major < 3:
        import dill
    turnman = Turnman(Entity())
    pickle.dumps(turnman)

class EmptyController(Controller):
    def act(self):
        return False

class PassController(Controller):
    def act(self):
        return None

class Counter(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('small', 0)
        self.dynamic_property('big', 0)
    @unbound
    def big_turn(self):
        self.big += 1
    @unbound
    def small_turn(self):
        self.small += 1

def test_empty_controller():
    turnman = Turnman(Counter())
    acting = PassController(None)
    empty = EmptyController(None)
    turnman.add_side(acting)
    turnman.add_side(empty)
    turnman.step()
    assert turnman.world.big == 0
    assert turnman.world.small == 1
    turnman.step()
    assert turnman.world.small == 2
    turnman.step()
    turnman.step()
    assert turnman.world.small == 2
    assert turnman.world.big == 0
