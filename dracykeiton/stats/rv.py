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
        return float(self.mean())
    
    def __int__(self):
        return int(float(self))
    
    def mean(self):
        return self.calculate(lambda x: x.mean())
    
    def rvs(self):
        return self.calculate(lambda x: x.rvs())
    
    def cdf(self, x):
        if not self._values:
            return float(self.calculate() <= x)
        if len(self._values) > 1:
            raise RVCdfError('cdf can only be calculated for RV with one distribution')
        rv = list(self._values.values())[0]
        if self._expr != self.value_expr(rv):
            raise RVCdfError('cdf can only be calculated for pure RV (expr={})')
        return rv.cdf(x)
    
    def calculate(self, f=None):
        """Calculate expression after applying function f to each variable"""
        if f is None:
            f = lambda x: x
        values = dict(self._values)
        values.update({
            name:f(value)
                for name, value in self._values.items()
                    if name.startswith('a_')
        })
        return eval(self._expr, values)
    
    @staticmethod
    def value_expr(value, const=False):
        if isinstance(value, RV):
            return value._expr
        return '('+RV.value_name(value, const=const)+')'
    
    @staticmethod
    def value_name(value, const=False):
        prefix = 'a_' if not const else 'b_'
        return prefix+str(id(value))
    
    def add_value(self, value, const=False):
        self._values[self.value_name(value, const=const)] = value
    
    @staticmethod
    def apply(f, *args, **kwargs):
        self = RV()
        self.add_value(f, const=True)
        for arg in list(args)+list(kwargs.values()):
            if isinstance(arg, RV):
                self._values.update(arg._values)
        self._expr = '({}(*[{}], **{}))'.format(
            self.value_expr(f, const=True),
            ', '.join([self.value_expr(arg) for arg in args]),
            {name:self.value_expr(value) for name, value in kwargs.items()}
        )
        return self

class RVCdfError(NotImplementedError):
    pass
