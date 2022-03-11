# BINP29_project
One week project during the BINP29 course (Lund University)

## Description
This program takes an rsID as input and outputs an interactive map showing the minor allele freqeuncies (MAFs) in the populations from the 1000 Genome Project phase 3 data set. The data is accesed from the ENSEMBL data base via their REST API. The documentation and code of that is found on https://rest.ensembl.org/documentation/info/variation_id. When hovering over a population point, the MAF of that population will show and when clicking on it, more information will pop up (allele count, minor allele, MAF, population ID, population name, population info). In the legend's header the user is informed about the input rsID and its minor allele followed by the MAFs for each population and their colour code on the map.

## Dependencies
- python 3.9
- requests 2.27.1
- pandas 1.4.1
- geopandas 0.10.2
- folium 0.12.1.post1

These dependencies can be installed with [conda](https://docs.anaconda.com/anaconda/install/index.html) using the `binp29p_env.yml` environment file.

```bash
conda env create -f binp29p_env.yml
conda activate bindp29p
```

## Running the program plotMAFs_worldmap.py
The program utilizes the ENSEMBL REST API to access minor allele frequencies (MAFs) and outputs an html file which contains an interactive world map with the MAFs of each population in the 1000 Genome Project phase 3.

It is run like:

```bash
/path_to_file/plotMAFs_worldmap.py
```
The output for rs16 is:

![image](https://user-images.githubusercontent.com/68820705/157863961-43670d84-9308-4afc-9477-2c08b0a03a8f.png)

## Obtaining data about the populations
Through the ENSEMBL REST API, only the population IDs were accessed therefore further information about the populations was downloaded from https://www.internationalgenome.org/data-portal/population and the downloaded tsv file is part of this Git Repo.
The getting_pop_ids.py script was run to parse the file and output the data needed to run plotMAFs_worldmap.py.

## Author(s)
Dorottya Ralbovszki
