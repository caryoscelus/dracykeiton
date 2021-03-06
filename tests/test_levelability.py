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

from dracykeiton.compat import *
from dracykeiton.common import LevelAbility, Caller
from dracykeiton.common.sandbox.goblin import GoblinLeader, Goblin

def test_levelup():
    goblin = GoblinLeader()
    assert goblin.level == 1
    assert not goblin.has_mod(Caller)
    goblin.level = 2
    assert goblin.level == 2
    assert goblin.has_mod(Caller)

def test_xp_levelup():
    goblin = GoblinLeader()
    assert goblin.level == 1
    assert not goblin.has_mod(Caller)
    goblin.xp = 300
    assert goblin.level == 2
    assert goblin.has_mod(Caller)

def test_attribute_levelup():
    goblin = Goblin()
    assert goblin.level == 0
    assert goblin.level_points == 0
    assert goblin.dexterity == 0
    goblin.xp = 100
    assert goblin.level == 1
    assert goblin.level_points == 1
    goblin.increase_attribute('dexterity')()
    assert goblin.level_points == 0
    assert goblin.dexterity == 1
