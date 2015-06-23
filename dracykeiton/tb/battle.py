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

from ..compat import *

class BattleState(object):
    pass

class NotFinished(BattleState):
    def __str__(self):
        return 'Not finished'

class Finished(BattleState):
    def __str__(self):
        return 'Finished'

class Won(Finished):
    def __init__(self, winner):
        self.winner = winner
    
    def __str__(self):
        return 'Won by {}'.format(self.winner)
