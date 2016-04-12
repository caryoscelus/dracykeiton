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

"""Test encounter advanced menu"""

from dracykeiton.encounter.advanced_menu import AdvancedMenu
from dracykeiton.encounter.option import Option

class OptionTest(Option):
    def __init__(self, name):
        super(OptionTest, self).__init__()
        self.name = name

def test_menu():
    am = AdvancedMenu(OptionTest)
    am.option('test')
    available_option_names = [option.name for option in am.available_options()]
    assert 'test' in available_option_names
