# BINP29_project
One week project during the BINP29 course (Lund University)

## Description
This program takes an rsID as input and outputs an interactive map showing the minor allele freqeuncies (MAFs) in the populations from the 1000 Genome Project phase 3 data set. The data is accesed from the ENSEMBL data base via their REST API. The documentation and code of that is found on https://rest.ensembl.org/documentation/info/variation_id.

## Dependencies
- python 3.9
- requests 2.27.1
- pandas 1.4.1
- geopandas 0.10.2
- folium 0.12.1.post1

These dependencies can be installed with [conda](https://docs.anaconda.com/anaconda/install/index.html) using the `binp29p_env.yml` environment file.

```shell
conda env create -f binp29p_env.yml
conda activate bindp29p
```

## Running the program plotMAFs_worldmap.py
The program utilizes the ENSEMBL REST API to access minor allele frequencies (MAFs) and outputs an html file which contains an interactive world map with the MAFs of each population in the 1000 Genome Project phase 3. When hovering over a population point, the MAF of that population will show and when clicking on it, more information will pop up (allele count, minor allele, MAF, population ID, population name, population info, rsID).

It is run like:

```shell
python3 /path_to_file/plotMAFs_worldmap.py
```
The output for rs16 is:
![image](https://user-images.githubusercontent.com/68820705/159171499-56b99397-4587-45b5-be58-d5431040dc80.png)


Be aware that when interacting with the procued map, three populations in the UK are overlapped when not zooomed in.

## Obtaining data about the populations
Through the ENSEMBL REST API, only the population IDs were accessed therefore further information about the populations was downloaded from https://www.internationalgenome.org/data-portal/population and the downloaded tsv file is part of this Git Repo for reproducibility purposes.
The getting_pop_ids.py script was run to parse the tsv file and output the data that was used in plotMAFs_worldmap.py. Three populations (Tamil, Telugu and British) were all sampled in Birmingham and as a result have the exact same coordinates. To address this overlap issue, coordinates of two populations were sightly changed so they can be visible but only after zooming in to the area.

## References
Genomes Project, C., Auton, A., Brooks, L. D., Durbin, R. M., Garrison, E. P., Kang, H. M., . . . Abecasis, G. R. (2015). A global reference for human genetic variation. Nature, 526(7571), 68-74. doi:10.1038/nature15393
Marcus, J. H., & Novembre, J. (2016). Visualizing the geography of genetic variants. Bioinformatics, 33(4), 594-595. doi:10.1093/bioinformatics/btw643
Yates, A., Beal, K., Keenan, S., McLaren, W., Pignatelli, M., Ritchie, G. R. S., . . . Flicek, P. (2015). The Ensembl REST API: Ensembl Data for Any Language. Bioinformatics (Oxford, England), 31(1), 143-145. doi:10.1093/bioinformatics/btu613
Zerbino, D. R., Achuthan, P., Akanni, W., Amode, M R., Barrell, D., Bhai, J., . . . Flicek, P. (2017). Ensembl 2018. Nucleic Acids Research, 46(D1), D754-D761. doi:10.1093/nar/gkx1098

## Author(s)
Dorottya Ralbovszki
