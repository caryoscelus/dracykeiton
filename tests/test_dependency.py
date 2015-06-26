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
from dracykeiton.util.dependency import DependencyTree, DependencyLoopError

import pytest

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

def test_loop():
    tree = DependencyTree()
    tree.add_dep(None, 'a')
    tree.add_dep('a', 'b')
    tree.add_dep('b', 'a')
    with pytest.raises(DependencyLoopError):
        list(tree)

def test_collect():
    class Foo(object):
        def __init__(self, s):
            self.deps = []
            self.s = s
        def __repr__(self):
            return 'Foo({})'.format(self.s)
        def get_dep(self):
            return self.deps
        def add_dep(self, dep):
            self.deps.append(dep)
    a = Foo('a')
    b = Foo('b')
    c = Foo('c')
    d = Foo('d')
    a.add_dep(b)
    b.add_dep(c)
    b.add_dep(d)
    c.add_dep(d)
    tree = DependencyTree.collect(a, Foo.get_dep)
    r = list(tree)
    assert r.index(a) > r.index(b) > r.index(c) > r.index(d)
