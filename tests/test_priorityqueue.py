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

"""test priorityqueue.py"""

import pytest

from dracykeiton.util.priorityqueue import PriorityQueue

def test_plain():
    plain_queue = PriorityQueue()
    plain_queue.add(1)
    plain_queue.add(2)
    assert list(plain_queue) == [1, 2]

def test_normal():
    queue = PriorityQueue('early', 'normal', 'late')
    queue.add(2, 'normal')
    queue.add(3, 'late')
    queue.add(0, 'early')
    queue.add(1, 'early')
    assert list(queue) == [0, 1, 2, 3]

def test_default():
    queue = PriorityQueue('early', 'normal', default='normal')
    queue.add(2)
    queue.add(0, 'early')
    queue.add(3)
    queue.add(1, 'early')
    assert list(queue) == [0, 1, 2, 3]

def test_default_exception():
    queue = PriorityQueue('early', 'normal')
    with pytest.raises(TypeError):
        queue.add(0)

def test_bad_priority():
    queue = PriorityQueue()
    with pytest.raises(NameError):
        queue.add(0, 'bad')

def test_remove():
    queue = PriorityQueue('early', 'normal', default='normal')
    with pytest.raises(ValueError):
        queue.remove(3)
    queue.add(3)
    queue.remove(3)
    assert not list(queue)
    queue.add(5, 'early')
    queue.remove(5)
    assert not list(queue)

def test_multi_remove():
    queue = PriorityQueue()
    queue.add(1)
    queue.add(1)
    assert len(queue) == 2
    queue.remove(1)
    assert len(queue) == 1
    queue.remove(1)
    assert len(queue) == 0
