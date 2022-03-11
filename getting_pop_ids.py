#!/usr/bin/python3
"""
Title: getting_pop_ids.py
Date: 2022-03-10
Author(s): Dorottya Ralbovszki

Description:
  This program opens and parses a tsv file containing population information of the 1000 Genome Project phase 3 release populations.
  When the lines are iterated, data is saved into lists and then these lists are printed to the standard output.
  These lists were then used to populate a dictionary in plotMAFs_worldmap.py.
  The input file opened in this program was downloaded from https://www.internationalgenome.org/data-portal/population.

List of functions:
    No user diefined functions are used in the program.

List of "non standard" modules:
    No "non standard" modules were used in the program.

Procedure:
    1. Empty lists are set up.
    2. The input file is opened.
    3. Lines in the input file are iterated in a for loop.
    4. The header line is passed.
    5. Rest of the lines are split into columns.
    6. Data from certain columns are saved into the lists.
    7. The lists are printed to standard output.
    

Usage:
    ./getting_pop_ids.py input.tsv
    
"""

import sys

# setting up emty lists
elasticid = []
popname = []
popinfo = []
latitude = []
longitude = []

# opening the input file
with open(sys.argv[1], 'r') as fin:
    for line in fin: # iterating through the lines in the input file
        if line.startswith('Population'): # the header line is passed
            continue
        else:
            line = line.rstrip() # removing \n character from the line
            line = line.split('\t') # splitting the line into columns, string becomes a list
            # accessing elemenst in the list and saving them in the previously set up lists
            elasticid.append(line[1]) 
            popname.append(line[2])
            latitude.append(line[4])
            longitude.append(line[5])
            popinfo.append(line[3])

# printing the lists into standard output
print(popname)
print(elasticid)
print(latitude)
print(longitude)
print(popinfo)