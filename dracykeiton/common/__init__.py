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

"""common: package containing common enitty build blocks"""

import importlib

__all__ = [
    'accuracy',
    'actor',
    'ap',
    'attribute',
    'battlefield',
    'calling',
    'container',
    'dice',
    'dexterity',
    'evasion',
    'grid',
    'heal',
    'hit',
    'hp',
    'inspire',
    'inventory',
    'kill',
    'level',
    'meta',
    'money',
    'variables',
    'xp',
    'xy',
]

# BLACK MAGIC
# import * from __all__
from . import *

for module in __all__:
    m = globals()[module]
    
    try:
        all_attrs = m.__all__
    except AttributeError:
        all_attrs = [name for name in dir(m) if name[0] != '_']
    for name in all_attrs:
        globals()[name] = getattr(m, name)
