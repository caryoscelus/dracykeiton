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

"""Test random hit action"""

from dracykeiton.compat import *

from dracykeiton.common import RandomHit

def test_random_hit():
    hitter = RandomHit()
    hitter.hit_damage = 6
    hit0 = hitter.hit_damage
    hit1 = hitter.hit_damage
    assert 4 <= hit0 <= 8
    assert 4 <= hit1 <= 8
    assert hit0 != hit1
