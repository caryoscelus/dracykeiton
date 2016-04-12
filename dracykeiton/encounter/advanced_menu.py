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

"""Generic parts of encounter advanced menu"""

from .option import Option

class Requirement(object):
    """Requirement & price for encounter option.
    
    Subclass this for your requirements
    """
    def check(self):
        """Check if requirement is satisfied."""
        return False
    
    def pay(self):
        """Pay the price of the option.
        
        This is called if Requirement is satisfied and option is chosen. No
        additional checks should be performed at this stage: they should go in
        .check()
        """
        pass

class AdvancedMenu(object):
    """Central class for encounter advanced menu.
    
    Usage example:
    ```
    am = AdvancedMenu()
    ...
    am.start('choice')
    am.option(...)
    am.set_option_custom_property(...)'
    ...
    am.option(...)
    ...
    ```
    """
    option_class = Option
    def __init__(self, option_class=None):
        super(AdvancedMenu, self).__init__()
        if option_class:
            self.option_class = option_class
        self.caption = None
        self.options = list()
        self.active_option = None
    
    def __getattr__(self, name):
        return getattr(self.active_option, name)
    
    def start(self, caption):
        """Clean advanced menu & set caption."""
        self.caption = caption
        self.options = list()
        self.active_option = None
    
    def option(self, *args, **kwargs):
        """Add option of class .options_class
        
        Additional arguments are passed to constructor. This option
        becomes active and all subsequent calls of unknown methods are
        directed to it.
        """
        self.active_option = self.option_class(*args, **kwargs)
        self.options.append(self.active_option)
