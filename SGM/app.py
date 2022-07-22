#!/usr/bin/env python
# Python 3.8.1

import pandas as pd

import server
import exceptions

json_input = {"code1": "shA", "code2": "W"}

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
            u_path = input("Enter the path and filename -> ") # open the dialog
            """Validating json_input by regular expression."""
            server.check_json(json_input)
            # this block can be removed, made to check the list of json
            if type(json_input) == list:
                input_df = pd.DataFrame.from_records(json_input, )
            else:
                input_df = pd.DataFrame([json_input])
            df = pd.read_csv(u_path)
            """Add new column 'bitCode', 'siCode' and add data to DataFrame"""
            result = server.add_columns(df)
            
            result = server.filter_data(input_df, df)
            return result

        except Exception as e:
                """exceptions can be handled later in this block"""
                print(e)


def test():
    print(csv_data(json_input))


if __name__ == '__main__':
    test()