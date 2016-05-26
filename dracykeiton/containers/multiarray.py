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

"""Contains MultiArray class"""

from ..compat import *
from ..util.curry import curry

class MultiArray(object):
    """Dynamic multi-dimensional `array`.
    
    Currently implemented with nested dictionaries.
    """
    fail = object()
    def __init__(self, dimensions):
        if dimensions < 1 or not isinstance(dimensions, int):
            raise ValueError('`dimensions` should be positive integer, not {}'.format(dimensions))
        self.dimensions = dimensions
        self._bounds = [(0, -1) for d in range(dimensions)]
        self._data = dict()
        self.empty = self.fail
    
    def _check_dimensions(self, d):
        if d != self.dimensions:
            raise IndexError('dimension mismatch (expecting {}, got {})'.format(self.dimensions, d))
    
    def __getitem__(self, coords):
        try:
            iter(coords)
        except TypeError:
            coords = (coords,)
        self._check_dimensions(len(coords))
        for d in range(self.dimensions):
            bounds = self._bounds[d]
            if not (bounds[0] <= coords[d] <= bounds[1]):
                raise IndexError('out of boundaries (dimension {}: {} is not in range [{}, {}]'.format(d, coords[d], bounds[0], bounds[1]))
        data = self._data
        for d in range(self.dimensions):
            try:
                data = data[coords[d]]
            except KeyError:
                if self.empty is self.fail:
                    raise ValueError('Empty at {} and empty policy is `fail`'.format(coords))
                if callable(self.empty):
                    new_value = self.empty(coords=coords)
                    self._setitem(coords, new_value)
                    return new_value
                return self.empty
        return data
    
    def _setitem(self, coords, value):
        """Set item without any checks"""
        data = self._data
        for d in range(self.dimensions-1):
            if not coords[d] in data:
                data[coords[d]] = {}
            data = data[coords[d]]
        data[coords[-1]] = value
    
    def __setitem__(self, coords, value):
        try:
            iter(coords)
        except TypeError:
            coords = (coords,)
        try:
            self[coords]
        except ValueError:
            pass
        self._setitem(coords, value)
    
    def _for_dimensions(self, f, ds):
        self._check_dimensions(len(ds))
        for d in range(self.dimensions):
            f(d, ds[d])
    
    def set_min(self, d, min):
        self._bounds[d] = (min, self._bounds[d][1])
    
    def set_mins(self, *mins):
        self._for_dimensions(self.set_min, mins)
    
    def set_max(self, d, max):
        self._bounds[d] = (self._bounds[d][0], max)
    
    def set_maxs(self, *maxs):
        self._for_dimensions(self.set_max, maxs)
    
    def set_bound(self, d, bound):
        if len(bound) != 2 or not all(isinstance(x, int) for x in bound):
            raise ValueError('boundaries should be tuple of two ints, not {}'.format(bound))
        self._bounds[d] = tuple(bound)
    
    def set_bounds(self, *bounds):
        self._for_dimensions(self.set_bound, bounds)
    
    def len(self, d):
        """Return length of array in given dimension"""
        bound = self._bounds[d]
        return max(bound[1]-bound[0]+1, 0)
    
    def lens(self):
        """Return list of current array lengths in all dimensions"""
        return [self.len(d) for d in range(self.dimensions)]

def dMultiArray(n):
    """Create MultiArray constructor with given dimensions."""
    return curry(MultiArray)(n)
