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

"""
"""

from ..compat import *
import functools

def wraps(f):
    """Version of functools.wraps with more helpful error message"""
    def decorator(*args, **kwargs):
        f0 = functools.wraps(f)
        try:
            return f0(*args, **kwargs)
        except AttributeError:
            raise AttributeError("AttributeError while wrapping for curry. It is likely you're passing a bad callable to curry.")
    return decorator

def update_wrapper(target, source):
    """Version of functools.update_wrapper with more helpful error message"""
    try:
        return functools.update_wrapper(target, source)
    except AttributeError:
        raise AttributeError("AttributeError while wrapping for curry. It is likely you're passing a bad callable to curry.")

def curry(f):
    """Takes a function and returns callable which returns callable.
    
    >>> cint = curry(int)
    >>> cint(base=2)('101')
    5
    >>> pprint = curry(print)('*')
    >>> pprint(1)
    * 1
    >>> pprint.__name__
    'print'
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        return update_wrapper(functools.partial(f, *args, **kwargs), f)
    return wrap
