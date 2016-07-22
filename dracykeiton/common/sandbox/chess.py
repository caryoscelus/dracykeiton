##
##  Copyright (C) 2015-2016 caryoscelus
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

from ...compat import *

from ...entity import Entity, mod_dep
from ..grid import GridEntity, GridField
from ..battlefield import BattlefieldEntity, Side
from ..hp import Living

@mod_dep(BattlefieldEntity, GridEntity, Living)
class ChessPiece(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('do_check_move', None)
    
    @unbound
    def check_move(self, x, y):
        return self.do_check_move(self, x, y)

@mod_dep(ChessPiece)
class Knight(Entity):
    @unbound
    def _init(self):
        def check_move(self, x, y):
            dx, dy = x-self.x, y-self.y
            return abs(dx)+abs(dy) == 3 and abs(dx) and abs(dy)
        self.do_check_move = check_move

@mod_dep(ChessPiece)
class Bishop(Entity):
    @unbound
    def _init(self):
        def check_move(self, x, y):
            dx, dy = x-self.x, y-self.y
            return abs(dx) == abs(dy) and dx
        self.do_check_move = check_move

@mod_dep(ChessPiece)
class Rook(Entity):
    @unbound
    def _init(self):
        def check_move(self, x, y):
            return (x and not y) or (y and not x)
        self.do_check_move = check_move


@mod_dep(GridField)
class ChessBoard(Entity):
    @unbound
    def _init(self):
        self.size = (8, 8)
        self.add_side('white', Side())
        self.add_side('black', Side())
