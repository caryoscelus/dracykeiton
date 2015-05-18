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

"""Ren'py compatibility layer. Exports Savable and HAS_RENPY.

If renpy is present, Savable is object from renpy.store, otherwise
just a regular object (which means it won't be actually savable).
In future this module may actually provide savable baseclass if
Ren'py is unavailable.
"""

try:
    from renpy.store import object as Savable
    HAS_RENPY = True
except ImportError:
    from builtins import object as Savable
    HAS_RENPY = False
