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

"""Local variables concept

Currently this is used for garbage-collecting ren'py namespace.
"""

from ..compat import *
from ..entity import Entity, properties

@properties(locals=set, callbacks=list)
class LocalVariables(Entity):
    """Entity containing local variable names.
    
    The values are not saved - the point is to have list of names.
    """
    def define_var(self, name):
        """Define local variable."""
        self.locals.add(name)
    
    def add_var_destroy_callback(self, callback):
        """Add callback to be launched on destroy()
        
        callback should be a callable accepting one argument: variable name
        """
        self.callbacks.append(callback)
    
    def destroy_vars(self):
        """Call destroy callback for variables."""
        for name in self.locals:
            for callback in self.callbacks:
                callback(name)
        self.locals.clear()
