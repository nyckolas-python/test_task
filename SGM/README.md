## 🎬👀 How it works

[![asciicast](https://asciinema.org/a/PI9szZPfwWPmxphMmtI9TnUrt.svg)](https://asciinema.org/a/PI9szZPfwWPmxphMmtI9TnUrt)

## ⚙️ Run locally

1. Clone this repo and enter to the project folder SGM:
```
git clone copy/paste/link/to/repo

cd SGM
```

2. Install Poetry is a tool for dependency management and packaging in Python:
```
$ make install poetry
# or
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
3. Install all dependencies:
```
$ make update
# or
$ poetry update
```
4. Run the 
```
$ make start
# or
$ poetry run python app.py
```

## ✅ Task

At this task you will be evaluated by the following criteria sorted by priority: 
1. SQL knowledge. 
2. Data processing. 
3. Basic pandas library knowledge (or research and learning skills, if you are not familiar with pandas) 
 
Documentation for the pandas library: 
https://pandas.pydata.org/docs/getting_started/index.html#getting-started 
 
For the test task you are going to use the .csv data file (db_table.csv) as the database table. This is your 
test data table. 
To get data from the file and store it in RAM, use pandas.read_csv('db_table.csv'). 
 
You are allowed to create your own database with data from .csv file. But you are also welcomed to use 
pandasql (https://pypi.org/project/pandasql/) - syntax and all the logic as for the real query to a data 
table. Choose what is more rational and effective for your approach. 
Make as less queries as you can, remember about an optimization and avoid extra connections. 
 
What is not allowed: 
▪  Add/modify/delete data from the original dataset. 
▪  (If database created) Create new datatable(s) to store processed data. 
 
Columns in the data file: 
date – date that corresponds to value. 
updateDate – date of the pushing data to database. 
code1, code2, code3 – data parameters. 
value – double precision format value. 
source – where data comes from. 
 
Extra columns (you will need to add extra data to your output): 
bitCode – 0 or 1. bitCode equals 1 if source equals S1, otherwise it is 0. 
siCode – if bitCode equals 1: A if code3 is AP or AH, B if code3 is PRD, BpA if code3 is YLD, otherwise 
undefined (None); if bitCode equals 0: H if code3 is AP or AH, T if code3 is PRD, TpH if code3 is YLD, 
otherwise undefined (None). 
 
Short naming across the test task: 
General code1 variable (G_code1): sh + 1 uppercase symbol. Example (G_code1 – code1): shA – sh + A. 
General code2 variable (G_code2): uppercase character/string before '/' symbol or, if no '/' (separator 
symbol) – value itself. Example (G_code2 - code2): W – W/WIN; S – S/1; C – C. 
 
Input (request from the frontend side): {"code1": #G_code1#, "code2": #G_code2#} 
Output (response from your side):  
1.  list of all sources for all possible requests. Format:  
{(#G_code1#, #G_code2#): [#source1#, #source2#, ..., #sourceN#]}  
2.  filtered and grouped data for each source from the previous step. You should return values of 
these columns: updateDate, code1, code2, code3, value + add two columns as for the condition 
above (siCode, bitCode). Format: 
 {(#G_code1#, #G_code2#, #sourceK#): [data rows]}  
Note: 
You need to return a result for all code1 and code2 values (among filtered for G values data). Not only 
when code1 equals G_code1 or code2 equals G_code2. 
 
Possible input: 
```
a)  {"code1": "shA", "code2": "W"} 
b)  {"code1": "shA", "code2": "S"} 
c)  {"code1": "shA", "code2": "C"} 
d)  {"code1": "shB", "code2": "W"} 
e)  {"code1": "shB", "code2": "S"} 
f)  {"code1": "shB", "code2": "C"} 
g)  {"code1": "shC", "code2": "W"} 
h)  {"code1": "shC", "code2": "S"} 
i)  {"code1": "shC", "code2": "C"} 
```
