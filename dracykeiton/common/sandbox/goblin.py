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

from ...entity import Entity
from ...compat import *
from .. import ActionPointEntity, HpEntity, InspirableHittingEntity, Battlefield, Side, InspiringEntity, KindEntity, XpLevelEntity, LivingActingEntity, XpKillingEntity, RobustHpEntity, LevelHpEntity, RoundingHpEntity

class Goblin(Entity):
    @unbound
    def _init(self):
        self.req_mod(HpEntity, 5)
        self.req_mod(RoundingHpEntity)
        self.req_mod(ActionPointEntity, 4)
        self.req_mod(LivingActingEntity)
        self.req_mod(InspirableHittingEntity, 3)
        self.req_mod(KindEntity, 'goblin')
        self.req_mod(XpLevelEntity, 0)
        self.req_mod(XpKillingEntity)
        self.req_mod(LevelHpEntity)
        self.req_mod(RobustHpEntity, 1.0)

class GoblinLeader(Entity):
    @unbound
    def _init(self):
        self.req_mod(Goblin)
        self.req_mod(InspiringEntity)
        self.level = 1
        self.robust = 0.8
