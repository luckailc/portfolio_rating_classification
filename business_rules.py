import pandas as pd
import utils

load_as_type_dict = {"PARTYFORMPUBLICREGISTRY": str,
                     "PARTYSUBFORMPUBLICREGISTRY": str,
                     "SEGMENT": str,
                     "INDUSTRY": str}
df = pd.read_csv("C:/Users/lucka/PycharmProjects/portfolio_rating_classification/datasets/brec_party.csv", dtype = load_as_type_dict)


# Codes from different sources assigned to different rating segment types
# A dictionary of entities form types from AJPES registry assigned to different rating types
dict_public_registry_type = {"LEGAL_ENTITIES": ["101", "102", "103", "104", "108", "112", "113", "117", "118", "142", "352", "706"],
                             "BANKS": ["704"],
                             "CENTRAL_GOVERNMENT": ["201", "300", "301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "313", "315", "321", "322"],
                             "ASSOCIATIONS": ["354", "355", "357", "406", "407", "453", "456"],
                             "FARMERS_A": ["148", "163"], # Farmers defined directly from public registry
                             "FARMERS_B": ["101", "102", "103", "104", "117", "142", "801", "802", "804", "807"], # Farmers defined indirectly e.g. agricultural company could be sorted into LEGAL_ENTITIES but because of the industry they operate in it is defined as FARMERS
                             "NEWLY_ESTABLISHED": ["101", "102", "103", "104", "108", "112", "113", "117", "118", "142", "352", "354", "355", "357", "406", "407", "453", "456", "706"],
                             "MUNICIPALITIES": ["316", "318", "319"],
                             "INSURANCE_COMPANIES": ["211"],
                             "LICENSED_PROFESSIONALS": ["119", "146", "151", "152", "153", "154", "155"],
                             "FOREIGN_COMPANIES": ["120", "141"],
                             "OTHER": ["143", "144", "145", "147", "156", "157", "158", "160", "166", "167", "210", "213", "358", "359", "360", "361", "362", "401", "402", "403", "404", "405", "451", "452", "458", "702", "703", "704", "706", "707", "708", "709", "710", "713", "714", "715", "718", "719", "799", "801", "802", "803", "804", "806", "807", "809", "810", "899"]}

# A dictionary of entities subform type from AJPES registry assigned to different rating types
dict_public_registry_subtype = {"BANKS": ["005"],
                                "INSURANCE_COMPANIES": ["006"],
                                "LICENSED_PROFESSIONALS": ["003"]}

# A dictionary of entities form type from NLB d.d. registry assigned to different rating types
dict_local_registry_type = {"BANKS": ["117"],
                            "ASSOCIATIONS": ["218", "222"],
                            "FARMERS": ["116"],
                            "INSURANCE_COMPANIES": ["118", "321"],
                            "LICENSED_PROFESSIONALS": ["112", "114", "151", "152"],
                            "FOREIGN_COMPANIES": ["141", "411", "412", "413"]}

# A dictionary of entities consent type from NLB d.d. registry. Used to recognize nominal tax deducters
dict_consent_type = {"NOMINAL_TAX_DEDUCTER": ["1"]}

# A dictionary of entities type from NLB d.d. registry. Definitions are in custody of NLB global risk
dict_segment = {"LEGAL_ENTITIES": ["PO"],
                "BANKS": ["IN"],
                "CENTRAL_GOVERNMENT": ["CD", "MO"],
                "FARMERS": ["PO"],
                "NEWLY_ESTABLISHED": ["PO"],
                "MUNICIPALITIES": ["RD"],
                "OTHER": ["IS", "JS", "NP"]}

# A dictionary of entities industry type. Used to recognize farmers
dict_industry = {"FARMERS": ["01", "02", "03"]}

# A dictionary of rules used to recognize rating segment type. Used in function: determine_rating_segment_type
dict_rating_segment_type = {# Rule for determining class LEGAL_ENTITIES
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('LEGAL_ENTITIES', [])) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.SEGMENT.isin(dict_segment.get('LEGAL_ENTITIES', [])))": "LEGAL_ENTITIES",
                            # Rule for determining class BANKS
                            "df.PARTYSUBFORMPUBLICREGISTRY.isin(dict_public_registry_subtype.get('BANKS', [])) | "
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('BANKS', [])) |"
                            "df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.PARTYFORMLOCALREGISTRY.isin(dict_local_registry_type.get('BANKS', [])) |"
                            "df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.PARTYFORMLOCALREGISTRY.isnull() & df.SEGMENT.isin(dict_segment.get('BANKS', []))": "BANKS",
                            # Rule for determining class CENTRAL_GOVERNMENT
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('CENTRAL_GOVERNMENT', [])) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.SEGMENT.isin(dict_segment.get('CENTRAL_GOVERNMENT', [])))": "CENTRAL_GOVERNMENT",
                            # Rule for determining class ASSOCIATIONS
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('ASSOCIATIONS', [])) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.PARTYFORMLOCALREGISTRY.isin(dict_segment.get('ASSOCIATIONS', [])))": "ASSOCIATIONS",
                            # Rule for determining class FARMERS
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('FARMERS_A', [])) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('FARMERS_B', [])) & df.INDUSTRY.str[:2].isin(dict_industry.get('FARMERS', []))) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.PARTYFORMLOCALREGISTRY.isin(dict_segment.get('FARMERS', []))) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.SEGMENT.isin(dict_segment.get('FARMERS', [])) & df.INDUSTRY.str[:2].isin(dict_industry.get('FARMERS', [])))": "FARMERS",
 # manjka kriterij let      # Rule for determining class NEWLY_ESTABLISHED
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('NEWLY_ESTABLISHED', [])) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.SEGMENT.isin(dict_segment.get('NEWLY_ESTABLISHED', [])))": "NEWLY_ESTABLISHED",
 # manjka kriterij privol.  # Rule for determining class NOMINAL_TAX_DEDUCTER
                            # Rule for determining class MUNICIPALITIES
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('MUNICIPALITIES', [])) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.SEGMENT.isin(dict_segment.get('MUNICIPALITIES', [])))": "MUNICIPALITIES",
                            # Rule for determining class INSURANCE_COMPANIES
                            "df.PARTYSUBFORMPUBLICREGISTRY.isin(dict_public_registry_subtype.get('INSURANCE_COMPANIES', [])) | "
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('INSURANCE_COMPANIES', [])) |"
                            "df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.PARTYFORMLOCALREGISTRY.isin(dict_local_registry_type.get('INSURANCE_COMPANIES', [])) ": "INSURANCE_COMPANIES",
                            # Rule for determining class LICENSED_PROFESSIONALS
                            "df.PARTYSUBFORMPUBLICREGISTRY.isin(dict_public_registry_subtype.get('LICENSED_PROFESSIONALS', [])) | "
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('LICENSED_PROFESSIONALS', [])) |"
                            "df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.PARTYFORMLOCALREGISTRY.isin(dict_local_registry_type.get('LICENSED_PROFESSIONALS', [])) ": "LICENSED_PROFESSIONALS",
                            # Rule for determining class FOREIGN_COMPANIES
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('FOREIGN_COMPANIES', [])) |"
                            "df.PARTYFORMLOCALREGISTRY.isin(dict_segment.get('FOREIGN_COMPANIES', []))": "FOREIGN_COMPANIES",
                            # Rule for determining class OTHER
                            "df.PARTYFORMPUBLICREGISTRY.isin(dict_public_registry_type.get('OTHER', [])) |"
                            "(df.PARTYFORMPUBLICREGISTRY.isnull() & df.PARTYSUBFORMPUBLICREGISTRY.isnull() & df.SEGMENT.isin(dict_segment.get('OTHER', [])))": "OTHER"}

def determine_rating_segment_type(df):
    """
    Function determines rating segment type.
    Dataframe get extended for new columns for each segment type. Each entity get T/F if conditions are met or not.
    Each entity has at least one segment type, more than one rating segment type can be determined for single entity.
    If none of the types is determined entity gets value not defined.
    """
    df = utils.concat_df_over_columns(df, ["LEGAL_ENTITIES", "BANKS", "CENTRAL_GOVERNMENT", "ASSOCIATIONS", "FARMERS", "NEWLY_ESTABLISHED", "NOMINAL_TAX_DEDUCTER", "MUNICIPALITIES", "INSURANCE_COMPANIES", "LICENSED_PROFESSIONALS", "FOREIGN_COMPANIES", "OTHER", "NOT_DEFINED"],
                                   None, False)
    for k, v in dict_rating_segment_type.items():
        df.loc[eval(k), v] = True
    return df

df = determine_rating_segment_type(df)

print(df.to_string())