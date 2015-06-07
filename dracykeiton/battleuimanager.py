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

""""""

class BattleUIManager(object):
    # We expect two-side battle with only one side controlled by user!
    def __init__(self, turnman):
        super(BattleUIManager, self).__init__()
        self.turnman = turnman
        self.selected = None
        self.user_controller = [s for s in self.turnman.sides if isinstance(s, UserController)][0]
    
    def clicked(self, side, entity):
        # TODO: ugh, fix this
        controller = [s for s in self.turnman.sides if tuple(s.entities)[0] == side][0]
        if isinstance(controller, UserController):
            self.select(entity)
        else:
            self.attack(entity)
    
    def select(self, entity):
        self.selected = entity
    
    def attack(self, entity):
        if not self.selected:
            return
        if self.selected.living != 'alive':
            self.selected = None
            return
        action = self.selected.hit(entity)
        if action:
            self.do_action(action)
    
    def do_action(self, action):
        self.user_controller.do_action(action)
        self.turnman.turn()
    
    def end_turn(self):
        self.user_controller.end_turn()
        self.turnman.turn()
        self.turnman.turn()
