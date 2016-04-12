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

"""Advanced menu outcome classes"""

class Outcome(object):
    """Outcome for multi-outcome advanced menu"""
    def __init__(self):
        self.condition = None
    
    def set_result(self):
        """Implement this to store outcome result to be used in launch.
        
        Can accept any number of args or kwargs - they are passed unchanged
        """
        pass
    
    def launch(self):
        """This is called when outcome happens. Implement in your subclass."""
        pass

class LabelOutcome(Outcome):
    """Outcome storing a simple label"""
    def __init__(self):
        super(LabelOutcome, self).__init__()
        self.label = None
    
    def set_result(self, label):
        self.label = label
