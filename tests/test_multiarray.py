##
##  Copyright (C) 2016 caryoscelus
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

"""test MultiArray"""

from dracykeiton.containers import MultiArray

import pytest

def test_badd():
    with pytest.raises(ValueError):
        MultiArray(0)
    with pytest.raises(ValueError):
        MultiArray(1.0)

def test_mismatchd():
    arr = MultiArray(2)
    with pytest.raises(IndexError):
        arr[0]
    with pytest.raises(IndexError):
        arr[(0, 0, 0)]

def test_1d():
    arr = MultiArray(1)
    assert tuple(arr.lens()) == (0,)
    with pytest.raises(IndexError):
        arr[0]
    with pytest.raises(IndexError):
        arr[0] = 1
    arr.set_maxs(5)
    assert arr.lens()[0] == 6
    with pytest.raises(ValueError):
        arr[0]
    arr.set_mins(1)
    assert arr.lens()[0] == 5
    with pytest.raises(IndexError):
        arr[0]
    arr[2] = 1
    assert arr[2] == 1
    assert arr[(2,)] == 1
    arr.set_maxs(1)
    with pytest.raises(IndexError):
        arr[2]
    arr.set_bounds((-10, -2))
    arr[(-10)] = None
    arr[(-2)] = None

def test_2d():
    arr = MultiArray(2)
    arr.set_maxs(9, 9)
    for x in range(10):
        for y in range(10):
            arr[(x, y)] = (x, y)
    assert arr[(5, 6)] == (5, 6)
