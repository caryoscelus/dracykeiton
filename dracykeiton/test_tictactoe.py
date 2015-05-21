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

"""Tic-tac-toe as a test"""

from entity import Entity, EntityMod
from controller import Controller
from turnman import Turnman, SimpleSideTurnman

class Board(EntityMod):
    def __init__(self, w, h):
        super(Board, self).__init__()
        self.w = w
        self.h = h
    def enable(self, target):
        target.dynamic_property('board')
        target.board = [[None for x in range(self.w)] for y in range(self.h)]
        target.dynamic_method('mark_tile')
        target.mark_tile = type(self).mark_tile
    def mark_tile(self, x, y, side):
        self.board[y][x] = side

class TicTacToe(Entity):
    def __init__(self):
        super(TicTacToe, self).__init__()
        self.add_mod(Board(3, 3))

class Player(Entity):
    def __init__(self, side):
        super(Player, self).__init__()
        self.dynamic_property('side')
        self.side = side

class TTTAI(Controller):
    def act(self):
        if len(self.entities) != 1:
            raise TypeError('TTTAI controller can only control single side')
        self.world.mark_tile(1, 1, tuple(self.entities)[0].side)

def test_tictactoe():
    board = TicTacToe()
    turnman = SimpleSideTurnman(board)
    en_x = Player('x')
    pl_x = TTTAI(board, en_x)
    en_o = Player('o')
    pl_o = TTTAI(board, en_o)
    turnman.add_side(pl_x)
    turnman.add_side(pl_o)
    turnman.turn()
    assert board.board[1][1] == 'x'
