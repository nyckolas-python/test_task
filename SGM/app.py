#!/usr/bin/env python
# Python 3.8.1

import pandas as pd

import server
import exceptions

json_input = {"code1": "shC", "code2": "C"}

json_input_list = [{"code1": "shA", "code2": "W"},
                {"code1": "shA", "code2": "S"},
                {"code1": "shA", "code2": "C"},
                {"code1": "shB", "code2": "W"},
                {"code1": "shB", "code2": "S"},
                {"code1": "shB", "code2": "C"},
                {"code1": "shC", "code2": "W"},
                {"code1": "shC", "code2": "S"},
                {"code1": "shC", "code2": "C"}]


def csv_data(json_input):
    try:
        u_path = input("Enter the path and filename of press Enter if 'data/db_table.csv'-> ") # open the dialog
        # 'db_table.csv' by default
        u_path = 'data/db_table.csv' if u_path == '' else u_path
        
        """Validating json_input by regular expression."""
        json_input = server.check_json(json_input)

        df = pd.read_csv(u_path)
        
        """Add new column 'bitCode', 'siCode' and add data to DataFrame"""
        df = server.add_columns(df)
        
        """Result Looks Like {('shC', 'C'): ['S1', 'S2', 'S4']}"""
        source_dict = server.source_dict(json_input, df)
        
        """Result Looks Like {(#G_code1#, #G_code2#, #sourceK#): [data rows]}"""
        result_list = server.filter_data(source_dict, df)
        
        server.ask_output(source_dict, result_list)
        return
    except Exception as e:
        """exceptions can be handled later in this block"""
        print(e)
    
def csv_sql_data(json_input):
    try:
        u_path = input("Enter the path and filename of press Enter if 'data/db_table.csv'-> ") # open the dialog
        # 'db_table.csv' by default
        u_path = 'data/db_table.csv' if u_path == '' else u_path
        """Validating json_input by regular expression."""
        json_input = server.check_json(json_input)

        df = pd.read_csv(u_path)
        """Add new column 'bitCode', 'siCode' and add data to DataFrame"""
        df = server.add_columns_sql(df)
        """Result Looks Like {('shC', 'C'): ['S1', 'S2', 'S4']}"""
        source_dict = server.source_dict_sql(json_input, df) # 
        """Result Looks Like {(#G_code1#, #G_code2#, #sourceK#): [data rows]}"""
        result_list = server.filter_data_sql(source_dict, df)
        
        server.ask_output(source_dict, result_list)
        return

    except Exception as e:
            """exceptions can be handled later in this block"""
            print(e)


def test():
    csv_sql_data(json_input)


if __name__ == '__main__':
    test()