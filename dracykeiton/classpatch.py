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

"""Very basic registry for any info associated with class.

It's main purpose is to be used for instance patching, which is why it's
called classpatch, but it's pretty general and agnostic of specific actions.
It only stores whatever you tell it to store.
"""

from compat import *

classpatch_registry = dict()

def register(target_class, tp, patch):
    if not target_class in classpatch_registry:
        classpatch_registry[target_class] = dict()
    if not tp in classpatch_registry[target_class]:
        classpatch_registry[target_class][tp] = []
    classpatch_registry[target_class][tp].append(patch)

def get(cl, tp):
    if not cl in classpatch_registry:
        return []
    if not tp in classpatch_registry[cl]:
        return []
    return classpatch_registry[cl][tp]
