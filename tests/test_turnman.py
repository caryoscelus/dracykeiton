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

from dracykeiton.compat import *
from dracykeiton.tb.controller import Controller, ProxyController
from dracykeiton.tb.turnman import Turnman, LockableTurnman
from dracykeiton.entity import Entity

def test_pickle():
    from dracykeiton import pickle
    turnman = Turnman(Entity())
    t1 = pickle.loads(pickle.dumps(turnman))
    lockable_turnman = LockableTurnman(Entity())
    lt1 = pickle.loads(pickle.dumps(lockable_turnman))

class EmptyController(Controller):
    def act(self):
        return False

class PassController(Controller):
    def act(self):
        return None

def test_turnman():
    turnman = Turnman(None)
    player = PassController(None, None)
    enemy = PassController(None, None)
    assert turnman.next_side() is None
    turnman.add_side(player)
    turnman.add_side(enemy)
    assert turnman.next_side() == player
    turnman.turn()
    assert turnman.next_side() == enemy

class Counter(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('small', 0)
        self.dynamic_property('big', 0)
    @unbound
    def new_round(self):
        self.big += 1
    @unbound
    def new_turn(self):
        self.small += 1

def test_empty_controller():
    turnman = Turnman(Counter())
    acting = PassController(None, None)
    empty = EmptyController(None, None)
    turnman.add_side(acting)
    turnman.add_side(empty)
    assert turnman.next_side() is acting
    turnman.turn()
    assert turnman.world.big == 1
    assert turnman.world.small == 2
    assert turnman.next_side() is empty
    turnman.turn()
    assert turnman.world.small == 2
    turnman.turn()
    turnman.turn()
    assert turnman.world.small == 2
    assert turnman.world.big == 1
    assert turnman.next_side() is empty

class SimpleCounter(object):
    def __init__(self):
        self.n = 0
    
    def count(self):
        self.n += 1

def test_lockable_turnman():
    turnman = LockableTurnman(None)
    counter = SimpleCounter()
    side = ProxyController(None, None)
    turnman.add_side(side)
    side.do_action(counter.count)
    turnman.turn()
    assert counter.n == 1
    turnman.lock()
    side.do_action(counter.count)
    turnman.turn()
    side.do_action(counter.count)
    turnman.turn()
    assert counter.n == 1
    turnman.unlock()
    assert counter.n == 3
    side.do_action(counter.count)
    turnman.turn()
    assert counter.n == 4
