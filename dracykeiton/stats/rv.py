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

from scipy.stats.distributions import rv_frozen
from numbers import Number
from ast import literal_eval

class RV(object):
    """Random value with distribution supporting arithmetic operations.
    
    NOTE: current implementation uses eval, however it is built safe, unless
    changed from the outside.
    """
    def __init__(self, value=0):
        self._values = dict()
        if isinstance(value, RV):
            self._values = value._values
            self._expr = value._expr
        elif isinstance(value, rv_frozen):
            self.add_value(value)
            self._expr = self.value_expr(value)
        elif isinstance(value, Number):
            self._expr = '({0})'.format(value)
        else:
            raise TypeError('RV can only be initialized with RV, scipy random values or numeric values.')
    
    def __add__(self, other):
        return self.op('+', self, other)
    
    def __radd__(self, other):
        return self.op('+', other, self)
    
    def __sub__(self, other):
        return self.op('-', self, other)
    
    def __rsub__(self, other):
        return self.op('-', other, self)
    
    def __mul__(self, other):
        return self.op('*', self, other)
    
    def __rmul__(self, other):
        return self.op('*', other, self)
    
    def __truediv__(self, other):
        return self.op('/', self, other)
    
    def __rtruediv__(self, other):
        return self.op('/', other, self)
    
    def __div__(self, other):
        return self.op('/', self, other)
    
    def __rdiv__(self, other):
        return self.op('/', other, self)
    
    @staticmethod
    def op(op, a, b):
        try:
            self = RV(a)
        except TypeError:
            return NotImplemented
        
        if isinstance(b, RV):
            self._values.update(b._values)
            right = b._expr
        elif isinstance(b, rv_frozen):
            self.add_value(b)
            right = self.value_expr(b)
        elif isinstance(b, Number):
            right = '({})'.format(b)
        else:
            return NotImplemented
        
        self._expr = '({}{}{})'.format(self._expr, op, right)
        return self
    
    def __float__(self):
        return self.mean()
    
    def __int__(self):
        return int(float(self))
    
    def mean(self):
        return self.calculate(lambda x: x.mean())
    
    def rvs(self):
        return self.calculate(lambda x: x.rvs())
    
    def calculate(self, f=None):
        """Calculate expression after applying function f to each variable"""
        if f is None:
            f = lambda x: x
        self._values = {name:f(value) for name, value in self._values.items()}
        return eval(self._expr.format(**self._values))
    
    @staticmethod
    def value_expr(value):
        return '({'+RV.value_name(value)+'})'
    
    @staticmethod
    def value_name(value):
        return 'a_'+str(id(value))
    
    def add_value(self, value):
        self._values[self.value_name(value)] = value
