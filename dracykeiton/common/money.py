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

"""Money-related stuff"""

from ..compat import *
from ..entity import Entity, properties

@properties(money=0)
class Money(Entity):
    @unbound
    def pay(self, amount):
        if amount < 0:
            raise ValueError('attempt to pay negative value')
        self.money -= amount
        if self.money < 0:
            raise ValueError('{} is bankrupt! Balance: {}'.format(self, self.money))
    
    @unbound
    def spend_money(self, amount):
        if amount <= self.money:
            self.pay(amount)
            return True
        return False

@properties(payment=0)
class Payment(Entity):
    @unbound
    def receive_payment(self, other):
        other.money += self.payment
