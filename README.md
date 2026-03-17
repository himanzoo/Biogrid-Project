# Biogrid



## Overview
The aim of this project is to load and filter the raw data from test_data.tsv file into pandas DataFrame by normalized the column names and filtering the columns. Then import data from pandas DataFrame to Database (biogrid.db). Therefore, the class importer and class query will correctly passed the given tests ["pytest"].  

## Data Format:
The given test data (raw data) is in the table form (tsv file format):
This table contains rows and columns:

NOTE: I have made dummy data with the same data structure due to data protection and safety.

Biogrid ID    |  Interaction ID  |   Entries Gene Interactor A    |    Entries Gene Interactor B
------        |   ------         |    -------                     |     -------
XX            |   XX             |    XXX                         |     XXX


## Dependencies:

dependencies = ["pandas>=2.2.3", "sqlalchemy>=2.0.38"]

requires-python = ">=3.12"

tests = [
    "pytest>=8.3.4"
]


## Authors and acknowledgment
I am Hira Manzoor and I am the author of my project.

I acknowledge Mr. Christian and Mr. Fabian for supporting me in this project.
