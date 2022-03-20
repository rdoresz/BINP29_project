#!/usr/bin/python3
"""

Title: plotMAFs_worldmap.py
Date: 2022-03-10
Author(s): Dorottya Ralbovszki

Description:
  This program takes an rsID as input and outputs an interactive map showing the minor allele freqeuncies (MAFs) in the populations from the 1000 Genome Project phase 3 data set.
  The data is accesed from the ENSEMBL data base via their REST API. The documentation and code of that is found on https://rest.ensembl.org/documentation/info/variation_id.
  When hovering over a population point, the MAF of that population will show and when clicking on it, more information will pop up (allele count, minor allele, MAF, population ID, population name, population info).
  In the legend's header the user is informed about the input rsID and its minor allele followed by the MAFs for each population and their colour code on the map.

List of functions:
    make_geodf was soursed from https://www.martinalarcon.org/2018-12-31-d-geopandas/ and was modified in this script.

List of "non standard" modules:
    geopandas - GeoDataFrame
    geopandas - points_from_xy
    folium

Procedure:
    1. Input from user is saved as rsid and data is accesed through ensembl's REST API.
    2. The data is parsed in a for loop and the information needed (MAF of each 1000 Genomes Project phase 3 population) is accessed and saved into dictionary. Also, the minor allele is saved into a variable.
    3. The population names in the dictionary is cleaned up and then the dictionary is transformed into a data frame.
    4. A new data frame is created containing data only about the minor allele. Another data frame is created containing the instanses where the major allele frequency was 1.
    5. A data frame containing the population names and their geo location is created. The data was originally accessed using the getting_pop_ids.py, further documentation about this is found there.
    6. 2 data frames are created by merging the minor_allele and the population info data frames as well as by merging the major_allele data frame and the population info data frames.
    7. In the major_allele merged data frame (df5) the major alleles are changed to the minor allele, their frequency is set to 0 from 1 and their count is set to 0.
    8. The two data frames are merged and the column population is dropped because it is duplicate of ID column.
    9. Using the make_geodf function, a dataframe with geopoints is created using the coordinates information.
    10. Adding more information (minor allele and rsID) to the data frame to be shown on the popup on the map.
    11. A base map is created using the module folium.
    12. Utilizing the geopoints and the base map, an interactive map is plotted.
    13. The map is saved into an html file.

Usage:
    ./plotMAFs_worldmap.py
    Enter the rsID
    Press Enter
"""
# importing dependencies
import requests, sys
import pandas as pd
from geopandas import GeoDataFrame
from geopandas import points_from_xy
import folium

'''
1.
'''
rsid = input (" Please type in the rsID ") # User input is saved in rsid


# accessing data using the ensembl REST API, code was provided by their manual website https://rest.ensembl.org/documentation/info/variation_id
server = "https://rest.ensembl.org"
ext = "/variation/human/{}?pops=1".format(rsid)
 
r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
if not r.ok:
  r.raise_for_status()
  sys.exit()
 
decoded = r.json()

'''
2.
'''
mydict = dict() # creating empty dictionary for saving the data from the json data
count = 0 # setting up a counter

# iterating through the json data
for big in decoded:
    if 'minor_allele' in big: # saving the minor allele in a variable
        minorallele = decoded[big]
    if 'populations' in big: # accessing the dictionary in the json that we are interested in
        for keys in decoded[big]: # accessing the dictionary in the json that we are interested in
            for kulcs in keys: # accessing the dictionary in the json that we are interested in
               val = str( keys[kulcs]) # chaning the item in the dictionary to a string so we can handle it
               if val.startswith('1000'): # catching data that is from 1000 Genomes Project
                   count += 1 # increasing the counter
                   key = str(count) # populating mydict
                   mydict[key] = keys 
                  
'''
3.
'''
# iterating through the dictionary
for key, info in mydict.items():
    for data in info: # since each item is a dictionary we need a second loop to access those
        if 'population' in data: # catching the info about population
           longid = info[data].split(':') # cleaning up the population names
           info[data] = longid[2] # and saving them into the dictionary

# creating a data frame from the dictionary
d2 = pd.DataFrame(mydict)
  
# swap the columns with indexes
d2 = d2.transpose()

for i in d2['frequency']:
    y = str(round(i, 2))
    d2['frequency'] = d2['frequency'].replace([i],y)



'''
4.
'''

# creating a dictionary with minor alleles only
df_minor = d2[d2['allele'] == minorallele]

# creating a dictionary with data when only major allele was counted
df_major = d2[d2['allele'] != minorallele] # keeping rows with major allele
major = df_major['allele']
major_allele = major[2] #saving the major allele into a variable

df_major = df_major[df_major ['frequency'] == 1] # keeping rows with frequency of 1


'''
5.
'''

# creating lists of the data colums that we want to save (from the tsv file parsed in the getting_pop_id-py script)
elasticid = ['CHS', 'FIN', 'PUR', 'KHV', 'ACB', 'BEB', 'ASW', 'YRI', 'LWK', 'JPT', 'CEU', 'CHB', 'CDX', 'GIH', 'GWD', 'MSL', 'ESN', 'PJL', 'IBS', 'CLM', 'PEL', 'TSI', 'MXL', 'STU', 'ITU', 'GBR']
popname = ['Southern Han Chinese', 'Finnish', 'Puerto Rican', 'Kinh Vietnamese', 'African Caribbean', 'Bengali', 'African Ancestry SW', 'Yoruba', 'Luhya', 'Japanese', 'CEPH', 'Han Chinese', 'Dai Chinese', 'Gujarati', 'Gambian Mandinka', 'Mende', 'Esan', 'Punjabi', 'Iberian', 'Colombian', 'Peruvian', 'Toscani', 'Mexican Ancestry', 'Tamil', 'Telugu', 'British']
popinfo = ['Han Chinese South', 'Finnish in Finland', 'Puerto Rican in Puerto Rico', 'Kinh in Ho Chi Minh City, Vietnam', 'African Caribbean in Barbados', 'Bengali in Bangladesh', 'African Ancestry in Southwest US', 'Yoruba in Ibadan, Nigeria', 'Luhya in Webuye, Kenya', 'Japanese in Tokyo, Japan', 'Utah residents (CEPH) with Northern and Western European ancestry', 'Han Chinese in Beijing, China', 'Chinese Dai in Xishuangbanna, China', 'Gujarati Indians in Houston, TX', 'Gambian in Western Division, The Gambia - Mandinka', 'Mende in Sierra Leone', 'Esan in Nigeria', 'Punjabi in Lahore, Pakistan', 'Iberian populations in Spain', 'Colombian in Medellin, Colombia', 'Peruvian in Lima, Peru', 'Toscani in Italy', 'Mexican Ancestry in Los Angeles, California', 'Sri Lankan Tamil in the UK', 'Indian Telugu in the UK', 'British in England and Scotland']
latitude = ['23.133330', '60.170000', '18.400000', '10.780000', '13.100000', '23.700000', '35.483000', '7.400000', '-1.270000', '35.680000', '40.767000', '39.916666', '22.000000', '29.758900', '13.454876', '8.480000', '9.066660', '31.554606', '40.380000', '4.583330', '-12.040000', '42.100000', '34.054400', '52.489814', '52.486156', '52.486243']
longitude = ['113.266667', '24.930000', '-66.100000', '106.680000', '-59.620000', '90.350000', '-97.533330', '3.920000', '36.610000', '139.680000', '-111.890400', '116.383333', '100.780000', '-95.367700', '-16.579032', '-13.230000', '7.483333', '74.357158', '-3.720000', '-74.066666', '-77.030000', '12.000000', '-118.243900', '-1.903184', '-1.876920', '-1.890401']


# creating a dictionary from the lists
idsdict = {
    'population ID' : elasticid,
    'population name' : popname,
    'population info' : popinfo,
    'latitude' : latitude,
    'longitude' : longitude
    }

# creating a data frame from the dictionary
df3 = pd.DataFrame(idsdict)


'''
6.
'''

# merging the minor allele data frame with the population info data frame keeping the rows that were present in both
df4 = df_minor.merge(df3, how='inner', left_on=('population'), right_on=('population ID'))

# merging the major allele data frame with the population info data frame keeping the rows that were present in both
df5 =df_major.merge(df3, how='inner', left_on=('population'), right_on=('population ID'))


'''
7.
'''


df5['allele'] = df5['allele'].replace([major_allele], minorallele) # replacing the major alleles with minor alleles in the data frame
df5['frequency'] = df5['frequency'].replace([1],0) # replacing 1 with 0 in the frequency column
df5['allele_count'] = (df5['allele_count'] == 1).astype(int) # replacing allele counts with 0


'''
8.
'''

# joining the minor allele data frame and data frame with the frequency=0
df_all = pd.concat([df4, df5], ignore_index=True)

# removing the population column because it contains redundant information
df_all = df_all.drop(labels='population', axis=1)


'''
9.
'''

# creating a function to create GeoDataFrame from coordinates (code was sourced from https://www.martinalarcon.org/2018-12-31-d-geopandas/ and than modified)
def make_geodf(df, lat_col_name='latitude', lon_col_name='longitude'):
    """
    Take a dataframe with latitude and longitude columns, and turn
    it into a geopandas df.
    """
    
    df = df.copy()
    lat = df['latitude']
    lon = df['longitude']
    return GeoDataFrame(df, geometry=points_from_xy(lon, lat))

# calling the function to create the GeoDataFrame
geo_df = make_geodf(df_all)


# removing the population column because it contains redundant information
geo_df = geo_df.drop(labels='latitude', axis=1)

# removing the population column because it contains redundant information
geo_df = geo_df.drop(labels='longitude', axis=1)


'''
10.
'''

# adding new information to the data frame
i = len(geo_df.index) # checking the number or rows and saving the value

snp = [] # setting up empty list for rsID

# filling up the lists in a loop
for s in range(i): # making sure the lists are the same length as the number of rows in the data frame
    snp.append(rsid) # filling up the list with the rsID


# adding the lists as columns to the data frame    
geo_df['rsID'] = snp



'''
11.
'''


m = folium.Map(tiles='Stamen Toner') # a base map is created using folium


'''
12.
'''

# on top of the base map, the locations of populations is plotted as an interactive map
geo_df.explore(
     m=m, # pass the map object
     column="frequency", # make choropleth based on "frequency" column
     marker_kwds=dict(radius=10, fill=True), # make marker radius 10px with fill
     tooltip="frequency", # show "frequency" column in the tooltip
     tooltip_kwds=dict(labels=False), # do not show column label in the tooltip
     popup=True, # turning on the popup function
     legend=False,
     #legend_kwds= dict(caption= 'SNP: {} Minor allele: {}'.format(rsid, minorallele)), # adding a title to legend box showing the rsid of the query and its minor allele
     name="populations" # name of the layer in the map
)

m = folium.TileLayer('Stamen Toner', control=True).add_to(m)  # alternative tiles added using folium
m = folium.LayerControl().add_to(m)  # adding layer control using folium


'''
13.
'''

m.save('{}.html'.format(rsid)) # the plot is saved in an html file

print('Please be aware that there are 3 populations in the UK all sampled in Birmingham that are only visible after zooming in, thank you!')