import pandas as pd
import numpy as np

def concat_df_over_columns(df_org, col_names, def_dict_val, remaining_default=None):
    # this are just immutable objects - so it's OK
    remaining_default = np.array([remaining_default] * df_org.shape[0])
    if isinstance(def_dict_val, dict):
        # just fill with remaining_default for all columns not defined under def_dict_val
        def_dict_val = {**{item: remaining_default for item in col_names}, **def_dict_val}
    else:
        def_dict_val = {item: remaining_default for item in col_names}
    # exclude columns that are already defined
    def_dict_val = {k: v for k, v in def_dict_val.items() if k not in list(df_org.columns)}
    return pd.concat([df_org, pd.DataFrame(def_dict_val, index=df_org.index)], axis=1)