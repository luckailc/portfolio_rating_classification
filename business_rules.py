
import pandas as pd

df = pd.read_csv("C:/Users/lucka/PycharmProjects/portfolio_rating_classification/datasets/brec_party.csv")

def segment_type_for_rating(row):
    if row["PARTYFORMPUBLICREGISTRY"] in (101, 102, 103, 104, 108, 112, 113, 117, 118, 142, 352, 706):
        return "LEGAL_ENTITIES"
    if (row["PARTYFORMPUBLICREGISTRY"] == [] and row["PARTYSUBFORMPUBLICREGISTRY"] == [] and row["SEGMENT"] == "PO"):
        return "LEGAL_ENTITIES"
    if row["PARTYSUBFORMPUBLICREGISTRY"] == '005':
        return "BANKS"
    if row["PARTYFORMPUBLICREGISTRY"] == 704:
        return "BANKS"
    if (row["PARTYFORMPUBLICREGISTRY"] == [] and row["PARTYSUBFORMPUBLICREGISTRY"] == [] and row["PARTYFORMLOCALREGISTRY"] == 117):
        return "BANKS"
    else:
        return []

df['result'] = df.apply(segment_type_for_rating, axis=1)

print(df[["PARTYFORMPUBLICREGISTRY", "PARTYSUBFORMPUBLICREGISTRY", "SEGMENT", 'result']])


"""#alternative approach


def restruction(row):
    return row["RESTRUCTIND"] == "AF"

def is_restructured():
    return 'Y'

def restruction_2(row):
    return row["RESTRUCTIND"] == "a"

def is_not_restructured():
    return "N"

def no_value():
    return 0

def restructuring_status_indicator(row):
    if restruction(row):
        return is_restructured()
    else:
        no_value()

dataset['result'] = dataset.apply(restructuring_status_indicator, axis=1)

#print(dataset[["RESTRUCTIND", "PARTYID", 'result']])


class Rule:
    def __init__(self, restruction, is_restructured):
        self.restruction = restruction
        self.is_restructured = is_restructured

class RulesEngine:
    def __init__(self, rule):
        self.rule = rule

    def run(self, row):
        for rule in self.rule:
            if rule.restruction(row):
                return rule.is_restructured(row)

def glavna_funkcija(row):
        return RulesEngine(
            rule(restruction, is_restructured)
        ).run(row)

dataset['result'] = dataset.apply(glavna_funkcija, axis=1)

print(dataset[["RESTRUCTIND", "PARTYID", 'result']])
"""