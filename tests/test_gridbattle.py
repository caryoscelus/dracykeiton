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

"""Grid-based battle test.
"""

from dracykeiton.compat import *

from dracykeiton.common import GridField
from dracykeiton.common.sandbox.chess import Knight, Bishop, Rook, ChessBoard

def test_chess_moves():
    """Test chess piece movement"""
    board = ChessBoard()
    assert tuple(board.grid.lens()) == (8, 8)
    darknight = Knight()
    board.spawn('black', darknight)
    board.put_on(0, 0, darknight)
    assert board.grid[(0, 0)].get() == darknight
    assert darknight.x == 0 and darknight.y == 0
    assert darknight.check_move(1, 2)
    assert not darknight.check_move(2, 2)
    board.put_on(1, 2, darknight)
    assert board.grid[(1, 2)].get() == darknight
    assert board.grid[(0, 0)].get() is None
