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

"""Advanced menu option classes"""

from .outcome import Outcome

from collections import OrderedDict

class Option(object):
    def __init__(self):
        super(Option, self).__init__()
        self.requires = list()
    
    def can_do(self):
        return all([req.check() for req in self.requires])
    
    def pay_costs(self):
        for req in self.requires:
            req.pay()

class OutcomeOption(Option):
    """AdvancedMenuOption supporting various outcomes
    """
    
    """Which class to use for outcome storage."""
    outcome_class = Outcome
    
    def __init__(self):
        super(OutcomeOption, self).__init__()
        self.outcomes = OrderedDict()
        self.forced_conditions = OrderedDict()
    
    def force_outcome(self, name, condition):
        self.forced_conditions[name] = condition
    
    def outcome_condition(self, name, condition):
        if not name in self.outcomes:
            self.outcomes[name] = self.outcome_class()
        self.outcomes[name].condition = condition
    
    def outcome_result(self, name, *args, **kwargs):
        if not name in self.outcomes:
            self.outcomes[name] = self.outcome_class()
        self.outcomes[name].set_result(*args, **kwargs)

class RollOutcomeOption(OutcomeOption):
    """Option which outcome depends on rolls."""
    def __init__(self):
        super(RollOutcomeOption, self).__init__()
        self.roll_n = None
    
    def roll(self, n):
        """Set roll result"""
        self.roll_n = n
    
    def call_roll(self, n):
        """Roll n dices and call after_roll
        
        Implement this in your subclass.
        """
        self.after_roll()
    
    def launch(self):
        self.pay_costs()
        
        for name in self.forced_conditions:
            cond = self.forced_conditions[name]
            if callable(cond):
                cond = cond()
            if cond:
                self.after_roll(forced=name)
        
        if self.roll_n != None:
            if callable(self.roll_n):
                self.roll_n = self.roll_n()
            self.call_roll(self.roll_n)
        else:
            self.after_roll()
    
    def after_roll(self, result=None, forced=None):
        if forced:
            self.outcomes[forced].launch()
            return
        for outcome in self.outcomes.values():
            if outcome.condition is None or outcome.condition(result):
                outcome.launch()
                break

class APIOption(Option):
    """AdvancedMenuOption that automatically generates api.
    
    Inherit this and put list of Requirement classes into api_classes and
    you'll get automatic api for adding requirements, based on
    Requirement.api_name or __name__
    """
    
    api_classes = list()
    
    def __getattr__(self, name):
        for cl in self.api_classes:
            api_name = getattr(cl, 'api_name', cl.__name__)
            if api_name == name:
                def f(*args, **kwargs):
                    self.requires.append(cl(*args, **kwargs))
                return f
        raise AttributeError('no such attribute or api class: {}'.format(name))
