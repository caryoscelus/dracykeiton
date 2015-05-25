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

"""PriorityQueue: queue with optional priority

>>> plain_queue = PriorityQueue('early', 'normal', default='normal')
>>> plain_queue.add(1)
>>> plain_queue.add(2, 'early')
>>> plain_queue.add(3)
>>> list(plain_queue)
[2, 1, 3]

"""

from compat import *

class PriorityQueue(object):
    def __init__(self, *priorities, **kwargs):
        super(PriorityQueue, self).__init__()
        default = None
        if 'default' in kwargs:
            default = kwargs['default']
        if not priorities:
            if not default:
                default = 'default'
            priorities = (default,)
        elif len(priorities) == 1 and default is None:
            default = priorities[0]
        
        if default != None and not default in priorities:
            raise NameError('PriorityQueue: default is not in priority list')
        self.priorities = priorities
        self.default = default
        self.store = {p : [] for p in priorities}
    
    def __iter__(self):
        for p in self.priorities:
            for value in self.store[p]:
                yield value
    
    def add(self, value, priority=None):
        if priority is None:
            if self.default:
                priority = self.default
            else:
                raise TypeError('PriorityQueue: no default and no priority provided')
        if not priority in self.priorities:
            raise NameError('no such priority: {}'.format(priority))
        self.store[priority].append(value)
