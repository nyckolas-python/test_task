#!/usr/bin/env python
# Python 3.8.1
import pandas as pd
from typing import Dict, NamedTuple, Optional
import re

import exceptions

class Input(Dict):
    """Structure input"""
    code1: str
    code2: str
    G_code1: str
    G_code2: str


class Output(Dict):
    """Structure output"""
    G_code1: str
    G_code2: str
    source: str
    raw_data: list

def check_json(json_input: dict)-> dict:
    """Validating password by regular expression."""
    """For example below:"""
    """{"code1": "shA", "code2": "W"}"""
    """{"code1": "shB", "code2": "W"}"""
    if type(json_input) == list:
        [check_json(json) for json in json_input]
    else:    
        pattern = r"\{(\"|\')(code1){1}(\"|\'):\s+(\"|\')(sh)[A-Z](\"|\'),\s+(\"|\')(code2)(\"|\'):\s+(\"|\')[A-Z](\"|\')\}"
        regexp_result = re.match(pattern, json_input)
        if not regexp_result:
            raise exceptions.NotCorrectJsonMessage(
                "Not Correct format JSON input, please check.")
        return json_input

def add_columns(df: pd.DataFrame) ->pd.DataFrame:
    """Add new column 'bitCode' and data to DataFrame"""
    """bitCode – 0 or 1. bitCode equals 1 if source equals S1, otherwise it is 0."""
    
    df.loc[df['source'] == 'S1', 'bitCode'] = '1'
    df.loc[df['source'] != 'S1', 'bitCode'] = '0'
    
    """Add new column 'bitCode' and data to DataFrame"""
    """siCode – if bitCode equals 1: A if code3 is AP or AH, B if code3 is PRD,
    BpA if code3 is YLD, otherwise undefined (None);
    if bitCode equals 0: H if code3 is AP or AH, T if code3 is PRD,
    TpH if code3 is YLD, otherwise undefined (None)."""
 
    df.loc[(df['bitCode'] == '1') & (df['code3'] == 'AP'), 'siCode'] = 'A'
    df.loc[(df['bitCode'] == '1') & (df['code3'] == 'AH'), 'siCode'] = 'A'
    df.loc[(df['bitCode'] == '1') & (df['code3'] == 'PRD'), 'siCode'] = 'B'
    df.loc[(df['bitCode'] == '1') & (df['code3'] == 'YLD'), 'siCode'] = 'BpA'
    df.loc[(df['bitCode'] == '0') & (df['code3'] == 'AP'), 'siCode'] = 'H'
    df.loc[(df['bitCode'] == '0') & (df['code3'] == 'AH'), 'siCode'] = 'H'
    df.loc[(df['bitCode'] == '0') & (df['code3'] == 'PRD'), 'siCode'] = 'T'
    df.loc[(df['bitCode'] == '0') & (df['code3'] == 'YLD'), 'siCode'] = 'TpH'
    df.loc[pd.isnull(df['siCode']), 'siCode'] = None
    return df

def filter_data(input_df: pd.DataFrame, df: pd.DataFrame) -> dict:
    i=0
    filter_list = []
    for i in range (input_df.shape[0]):
        filter_df = df[(df['code1'].str[:3] == input_df['code1'][i]) & (df['code2'].str[:1] == input_df['code2'][i])]
    #   filter_list.append({(input_df['code1'][i], input_df['code2'][i]): (list(filter_df['source'].unique()), filter_df['source'].shape[0])})
        key = (input_df['code1'][i], input_df['code2'][i])
        value = list(filter_df['source'].unique())     
        filter_list.append({key: value})
        """Now filter_list looks like:
        [{('shC', 'C'): ['S1', 'S2', 'S4']}]"""
        
        result = {}

        if len(value) > 0:
            for j in value:
                raws_key = key + (j,)
                raw_data = df[(df['code1'].str[:3] == input_df['code1'][i]) & (df['code2'].str[:1] == input_df['code2'][i]) & (df['source'] == j)]
                value_raws = raw_data[ ['updateDate', 'code1', 'code2', 'code3', 'value', 'bitCode', 'siCode'] ].values.tolist()
                if result == {}:
                    result = {raws_key: value_raws}
                else:
                    result_list = []
                    result_list.append(result)
            return result if result_list == [] else result_list
        else:
            raise exceptions.DataFrameError(
                "Сan't filter the Data, please check your DataFrame input.")