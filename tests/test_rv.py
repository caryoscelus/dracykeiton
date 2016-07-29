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

"""Test random variables"""

from dracykeiton.stats.rv import RV
from scipy.stats import norm

def test_cast():
    assert int(RV(norm(loc=4))) == 4

def test_add():
    a = RV(norm(loc=1))
    b = RV(norm(loc=3.4))
    assert float(a+b) == 4.4

def test_sub_number():
    assert int(5-RV(norm(loc=3))) == 2

def test_complex_expr():
    a = RV(norm(loc=1))
    b = RV(norm(loc=3.4))
    c = RV(norm(loc=100))
    r = ((a*3.2+b)*c+1)/10
    print(r._expr)
    assert float(r) == 66.1
