#!/usr/bin/env python
# Python 3.8.1
import json
import pandas as pd
import pandasql as ps
import re

import exceptions

class InputJson():
    """Structure input. On the input:dict -> string atributes returns on the output

    code1: str	(first key of input:dict)
    
    code2: str	(second key of input:dict)
    
    G_code1: str	(first value of input:dict)
    
    G_code2: str	(second value of input:dict)
    
    json: dict	(original dictionary json)
    """
    def __init__(self, json_input:dict) -> str:
        self.code1 = str(list(json_input.keys())[0])
        self.code2 = str(list(json_input.keys())[1])
        self.G_code1 = str(list(json_input.values())[0])
        self.G_code2 = str(list(json_input.values())[1])
        self.json = json_input


class SourcesDict():
    """Structure output. On the input:dict -> atributes    
    
    G_code1: str	(first value of input:dict)
    
    G_code2: str	(second value of input:dict)
    source_list: List   (list of sources)
    json: dict	(original dictionary json)
    """
    def __init__(self,dict_input):
        self.G_code1 = str(list(dict_input.keys())[0][0])
        self.G_code2 = str(list(dict_input.keys())[0][1])
        self.G_code_tuple = list(dict_input.keys())[0]
        self.source_list = list(dict_input.values())[0]
        self.G_tuple = (self.G_code1, self.G_code2)
        self.json = dict_input


def check_json(json_input: dict)-> InputJson:
    """Validating json_input by regular expression."""
    """For example below:"""
    """{"code1": "shA", "code2": "W"}"""
    """{"code1": "shB", "code2": "W"}""" 
    pattern = r"\{(\"|\')(code1){1}(\"|\'):\s+(\"|\')(sh)[A-Z](\"|\'),\s+(\"|\')(code2)(\"|\'):\s+(\"|\')[A-Z](\"|\')\}"
    json_str = json.dumps(json_input)
    regexp_result = re.match(pattern, json_str)
    if not regexp_result:
        raise exceptions.NotCorrectJsonMessage(
            "Not Correct format JSON input, please check.")
    print("Validating json_input is OK ...")
    return InputJson(json_input)

def add_columns(df: pd.DataFrame) ->pd.DataFrame:
    """Add new column 'bitCode' and data to DataFrame"""
    """bitCode – 0 or 1. bitCode equals 1 if source equals S1, otherwise it is 0."""
    
    df.loc[df['source'] == 'S1', 'bitCode'] = '1'
    df.loc[df['source'] != 'S1', 'bitCode'] = '0'
    print("Add new column 'bitCode' and data is OK")
    
    """Add new column 'siCode' and data to DataFrame"""
    """'siCode' - if bitCode equals 1: A. if code3 is AP or AH, B if code3 is PRD,
    BpA if code3 is YLD, otherwise undefined (None);
    if bitCode equals 0: H if code3 is AP or AH, T if code3 is PRD,
    TpH if code3 is YLD, otherwise undefined (None)."""
    
    # Block below need Refactoring using methon or function
    df.loc[(df['bitCode'] == '1') & (df['code3'] == 'AP'), 'siCode'] = 'A'
    df.loc[(df['bitCode'] == '1') & (df['code3'] == 'AH'), 'siCode'] = 'A'
    df.loc[(df['bitCode'] == '1') & (df['code3'] == 'PRD'), 'siCode'] = 'B'
    df.loc[(df['bitCode'] == '1') & (df['code3'] == 'YLD'), 'siCode'] = 'BpA'
    df.loc[(df['bitCode'] == '0') & (df['code3'] == 'AP'), 'siCode'] = 'H'
    df.loc[(df['bitCode'] == '0') & (df['code3'] == 'AH'), 'siCode'] = 'H'
    df.loc[(df['bitCode'] == '0') & (df['code3'] == 'PRD'), 'siCode'] = 'T'
    df.loc[(df['bitCode'] == '0') & (df['code3'] == 'YLD'), 'siCode'] = 'TpH'
    df.loc[pd.isnull(df['siCode']), 'siCode'] = None
    print("Add new column 'siCode' and data is OK ...")
    return df

def source_dict(json_input: InputJson, df: pd.DataFrame) -> dict:
    """First step result like {('shC', 'C'): ['S1', 'S2', 'S4']}"""

    filter_df = df[(df['code1'].str[:3] == json_input.G_code1) & (df['code2'].str[:1] == json_input.G_code2)]
    key = (json_input.G_code1, json_input.G_code2)
    value = list(filter_df['source'].unique())     
    source_dict = SourcesDict({key: value})
    """Now we have source_dict looks like:
    {('shC', 'C'): ['S1', 'S2', 'S4']}"""
    return source_dict
    
def filter_data(source_dict: SourcesDict, df: pd.DataFrame) ->list:
    """Second step - filter data and get data frame"""
    """Result Looks Like {(#G_code1#, #G_code2#, #sourceK#): [data rows]}"""
    result_list = []
    if len(source_dict.source_list) > 0:
        for j in source_dict.source_list:
            raws_key = source_dict.G_tuple + (j,)
            raws_data = df[(df['code1'].str[:3] == source_dict.G_code1) & (df['code2'].str[:1] == source_dict.G_code2) & (df['source'] == j)]
            value_raws = raws_data[ ['updateDate', 'code1', 'code2', 'code3', 'value', 'bitCode', 'siCode'] ].values.tolist()
            result_list.append({raws_key: value_raws})
        print("Data filtered successfully ...")
        return result_list
    else:
        raise exceptions.DataFrameError(
            "Сan't filter the Data, please check your DataFrame input.")

def ask_output(source_dict:SourcesDict, result_list:list):
    u_path = input("press Enter to export -> 'list_of_sources.json' and 'data_source_N.json'")
    u_path_output = 'list_of_sources.json'
    
    with open(u_path_output, 'w') as f:
        # try:
            with open(u_path_output,'w') as out:
                # write file 'list_of_sources.json'
                out.write(f"{source_dict.json}")
                print(f"File '{u_path_output}' was write successfully ...")
        # except Exception as e:
        #     """exceptions can be handled later in this block"""
        #     print(e)
        
    for index,source in enumerate(source_dict.source_list):
        u_path_output = f"data_source_{source}.json"
        with open(u_path_output, 'w') as f:
            try:
                with open(u_path_output,'w') as out:
                    # write file 'data_source_N.json'
                    out.write(f"{result_list[index]}")
                    print(f"File 'data_source_{source}.json' was write successfully ...")

            except IndexError as e:
                    """exceptions can be handled later in this block"""
                    pass

def add_columns_sql(df: pd.DataFrame) -> pd.DataFrame:
    # use SQL 
    add_columns_query = '''
        SELECT *,
            CASE source WHEN 'S1' THEN '1' ELSE '0'
            END as bitCode,
            CASE
                WHEN source = 'S1' AND code3 IN ('AP', 'AH') THEN 'A'
                WHEN source = 'S1' AND code3 = 'PRD' THEN 'B'
                WHEN source = 'S1' AND code3 = 'YLD' THEN 'BpA'
                WHEN source <> 'S1' AND code3 IN ('AP', 'AH') THEN 'H'
                WHEN source <> 'S1' AND code3 = 'PRD' THEN 'T'
                WHEN source <> 'S1' AND code3 = 'YLD' THEN 'TpH'
                ELSE 'None'
            END as siCode
        FROM df;
        '''
    df = ps.sqldf(add_columns_query, locals())
    print("Add new column 'bitCode', 'siCode' and data is OK ...")
    return df

def source_dict_sql(json_input: InputJson, df: pd.DataFrame) -> dict:
    """Selects data"""
    """First step - select data from code1 and code2"""

    filter_sql_query = f'''
    SELECT DISTINCT (source)
    FROM df
    WHERE code1 LIKE '{json_input.G_code1}%' AND code2 LIKE '{json_input.G_code2}%';
    '''
    unique_source = ps.sqldf(filter_sql_query, locals())
    key = (json_input.G_code1, json_input.G_code2) # ('shC', 'C')
    value = unique_source['source'].tolist() # ['S1', 'S2', 'S4']
    source_dict = SourcesDict({key: value})
    print(f"List of sources {source_dict.json} is OK ...")
    return source_dict

def filter_data_sql(source_dict: SourcesDict, df: pd.DataFrame) ->list:
    """Second step - filter data and get data frame"""
    """Result Looks Like {(#G_code1#, #G_code2#, #sourceK#): [data rows]}"""
    
    result = {}
    result_list = []

    if len(source_dict.source_list) > 0:
        for source in source_dict.source_list:
            raws_key = source_dict.G_tuple + (source,)
            filter_query = f'''
            SELECT updateDate, code1, code2, code3, value, bitCode, siCode
            FROM df
            WHERE code1 LIKE '{source_dict.G_code1}%' AND code2 LIKE '{source_dict.G_code2}%' AND source = '{source}';
            '''
            raw_data = ps.sqldf(filter_query, locals())
            value_raws = raw_data.values.tolist()
            if result == {}:
                result = {raws_key: value_raws}
            else:
                result_list.append(result)
        print("Data filtered successfully ...")
        return result if result_list == [] else result_list
    else:
        raise exceptions.DataFrameError(
            "Сan't filter the Data, please check your DataFrame input.")