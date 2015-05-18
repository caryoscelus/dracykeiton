##
##  Copyright (C) 2015 caryoscelus
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

from priorityqueue import PriorityQueue

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
