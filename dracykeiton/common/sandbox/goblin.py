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

from ...entity import Entity, mod_dep
from ...compat import *
from .. import ActionPoint, Hp, InspirableHit, Battlefield, Side, Inspire, Kind, XpBasedLevel, LivingActing, XpKill, RobustHp, LevelHp, RoundingHp, Caller, LevelAbility, DexterityBasedAccuracy, DexterityBasedEvasion

@mod_dep(
    RoundingHp,
    ActionPoint,
    LivingActing,
    LevelHp,
    RobustHp,
    InspirableHit,
    Kind,
    XpKill,
    XpBasedLevel,
    DexterityBasedAccuracy,
    DexterityBasedEvasion
)
class Goblin(Entity):
    @unbound
    def _init(self):
        self.maxhp = 5
        self.maxap = 4
        self.hit_damage = 3
        self.kind = 'goblin'
        self.robust = 1.0
        self.xp = 0
        self.dexterity = 0

@mod_dep(Goblin, Inspire, LevelAbility)
class GoblinLeader(Entity):
    @unbound
    def _init(self):
        self.on_level(2, Caller, Goblin)
        self.level = 1
        self.robust = 0.8
