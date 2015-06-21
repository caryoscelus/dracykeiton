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

"""Module containing ActionProcessor, action decorator and related stuff.
"""

import functools

from .compat import *
from .util import curry

def action(f):
    """Decorator making callable which checks if action is possible.
    
    If it's possible, return actual action callable, else return None. Checker
    method should have same name prefixed with can_
    
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
    argcount = f.__code__.co_argcount
    wrap.arguments = f.__code__.co_varnames[:argcount]
    return wrap

class ActionProcessor(object):
    """Action processing entity.
    
    Could be asked to process action and either do it or not and maybe do
    something else as well.
    """
    def process(self, a):
        """Takes action and maybe processes it (and possibly side effects)
        
        Returns True if action was processed, False otherwise.
        """
        a()
        return True

class SimpleEffectProcessor(ActionProcessor):
    """Action processor capable of performing effects when actions happen."""
    def __init__(self):
        super(SimpleEffectProcessor, self).__init__()
        self.init_effects()
    
    def init_effects(self):
        self._effects = dict()
    
    def process(self, a):
        if a.__name__ in self._effects:
            for effect in self._effects[a.__name__]:
                effect(a)
        r = super(SimpleEffectProcessor, self).process(a)
        return r
    
    def add_effect(self, target, effect):
        """Add effect to be performed when action happens.
        
        NOTE: currently all effects will be performed in the same order as
        they were added in.
        """
        if not target in self._effects:
            self._effects[target] = list()
        self._effects[target].append(effect)
