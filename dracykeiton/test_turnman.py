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

from controller import Controller
from turnman import Turnman
from entity import Entity

def test_turnman():
    turnman = Turnman(None)
    player = Controller(None)
    enemy = Controller(None)
    turnman.add_side(player)
    turnman.add_side(enemy)
    #turnman.turn()
    player_c = Entity()
    enemy_c = Entity()
    player.add_entity(player_c)
    enemy.add_entity(enemy_c)

def test_pickle():
    import pickle
    import dill
    turnman = Turnman(Entity())
    pickle.dumps(turnman)
