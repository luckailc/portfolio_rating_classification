import pandas as pd
import business_rules
import calculations

if __name__ == "__main__":
    load_as_type_dict = {"PARTYNAME": str,
                         "PARTYFORMPUBLICREGISTRY": str,
                         "PARTYSUBFORMPUBLICREGISTRY": str,
                         "SEGMENT": str,
                         "INDUSTRY": str}
    df = pd.read_csv("C:/Users/lucka/PycharmProjects/portfolio_rating_classification/data/brec_party.csv",
                     dtype=load_as_type_dict)
    df = business_rules.determine_rating_segment_type(df)
    df = business_rules.rank_rating_segment_type(df)
    df = business_rules.determine_model_type(df)
    print(df.to_string())