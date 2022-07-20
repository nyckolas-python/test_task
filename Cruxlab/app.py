#!/usr/bin/env python
# Python 3.8.1
import re


u_path = input("Enter the path and filename -> ") # open the dialog

def validate_by_regexp(line: str) -> bool:
    """Validating password by regular expression."""
    """For example below:"""
    """b 3-6: bhhkkbbjjjb"""
    """b 1: bhhkkdfdkfjdj"""
    pattern = "(.+) ([\d]+)-*([\d]+)*: (.+)(/n)*"
    regexp_result = re.match(pattern, line)
    if not regexp_result or not regexp_result.group(0) \
        or not regexp_result.group(1) or not regexp_result.group(2) \
        or not regexp_result.group(4):
        return False
    elif not regexp_result.group(3) and int(regexp_result.group(2)) == \
        regexp_result.group(4).count(regexp_result.group(1)):
        return True
    elif int(regexp_result.group(2)) <= \
        regexp_result.group(4).count(regexp_result.group(1)) <= \
            int(regexp_result.group(3)):
        return True
    else:
        return False

def count_valid_pass() -> int:
    """Count of valid passwords"""
    with open(u_path, "r") as f:
          pass_list = f.readlines()
          try:
                result = sum([validate_by_regexp(line) for line in pass_list])
                #notvalid = [line for line in pass_list if validate_by_regexp(line) is False]
                #print(notvalid)
                #print(f"number of valid passwords is {result}")
          except Exception as e:
                """exceptions can be handled later in this block"""
                print(e)
    return result


def test():
    print(count_valid_pass())


if __name__ == '__main__':
    test()