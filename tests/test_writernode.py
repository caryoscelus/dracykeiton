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

"""Test writer node - mostly ensuring that it pickle/unpickles fine"""

from dracykeiton.compat import *
from dracykeiton.entity import Entity, writernode, simplenode, depends
from dracykeiton import pickle

class WriterEntity(Entity):
    @unbound
    def _init(self, initial=0):
        self.dynamic_property('core', initial)
        self.dynamic_property('writer')
        self.add_set_node('writer', self.write())
        self.add_get_node('writer', self.read())
    
    @writernode
    def write(self, value):
        self.core = value/2
        return None
    
    @depends('core')
    @simplenode
    def read(value, core):
        return core*2

def test_writer():
    writer = WriterEntity()
    writer.core = 5
    assert writer.writer == 10
    writer.writer = 6
    assert writer.writer == 6
    assert writer.core == 3

def test_writer_pickle():
    w0 = WriterEntity()
    w0.writer = 10
    w0.core += 4
    w1 = pickle.loads(pickle.dumps(w0))
    assert w1.core == 9
