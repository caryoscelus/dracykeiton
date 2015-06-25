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

"""Tests for dracykeiton.util.dependency"""

from dracykeiton.compat import *
from dracykeiton.util.dependency import DependencyTree

def test_deps():
    tree = DependencyTree()
    tree.add_dep(None, 'root')
    tree.add_dep('root', 'a')
    tree.add_dep('root', 'b')
    tree.add_dep('b', 'common')
    tree.add_dep('a', 'a0')
    tree.add_dep('a0', 'common')
    r = list(tree)
    assert r.index('common') == 0
    assert r.index('a0') < r.index('a')
    assert r.index('a') < r.index('root')
    assert r.index('b') < r.index('root')

def test_empty():
    tree = DependencyTree()
    assert list(tree) == []

def test_reuse():
    tree = DependencyTree()
    tree.add_dep(None, 'root')
    assert list(tree) == ['root']
    assert list(tree) == ['root']
