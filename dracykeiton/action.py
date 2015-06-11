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

import functools

from compat import *
import curry

def action(f):
    """Decorator making callable which checks if action is possible.
    
    If it's possible, return curry, else return None. Checker method
    should have same name prefixed with can_
    
    >>> from entity import Entity
    >>> class Foo(Entity):
    ...     @action
    ...     def bar(self, n):
    ...         print(n)
    ...     def can_bar(self, n):
    ...         return n > 0
    >>> foo = Foo()
    >>> foo.bar(5).__name__
    'bar'
    >>> foo.bar(5)()
    5
    >>> print(foo.bar(0))
    None
    """
    @functools.wraps(f)
    def wrap(self, *args, **kwargs):
        if getattr(self, 'can_{}'.format(f.__name__))(*args, **kwargs):
            return curry.curry(f)(self, *args, **kwargs)
        else:
            return None
    return wrap

class ActionProcessor(object):
    def process(self, a):
        a()
        return True

class SimpleEffectProcessor(ActionProcessor):
    """Action processor capable of performing effects when actions happen."""
    def __init__(self):
        super(SimpleEffectProcessor, self).__init__()
        self._effects = dict()
    def process(self, a):
        r = super(SimpleEffectProcessor, self).process(a)
        if a.__name__ in self._effects:
            self._effects[a.__name__](a)
        return r
    def add_effect(self, target, effect):
        self._effects[target] = effect
