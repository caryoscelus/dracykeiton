# dracykeiton

Dracykeiton [draʃəkɛjton] is yet another RPG-oriented gamedev
toolkit/library for Python. More specifically, it was created to be used
with Ren'Py, however it can be used stand-alone or in combination with
another libraries. Python 2 will be somewhat supported as long as Ren'Py
requires it, but otherwise it's Python 3 project.

Right now it's focused on battle-related stuff, since original purpose was
to create a battle engine for a specific Ren'Py project.

## testing

    # setup virtual environments for python 3..
    pyvenv env
    # ..and python 2
    virtualenv env2
    # install git hooks
    ln -s `pwd`/githooks/pre-commit .git/hooks/
    # launching tests
    ./run-all-tests.sh

## documentation

Coming soon. For now, look for docstrings.

## license

    Copyright (C) 2015 caryoscelus
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
