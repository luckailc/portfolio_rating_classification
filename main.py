# This is a sample Python script.

"""
Example how to use rule engine
"""

class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

class RulesEngine:
    def __init__(self, *rules):
        self.rules = rules

    def run(self, state):
        for rule in self.rules
            if rule.condition(state(:
                return rule.action(state)))
