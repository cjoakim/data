#!/bin/bash

# Exploring the opendatasoft HTTP API with curl

# See list of datasets here:
# - https://documentation-resources.opendatasoft.com/explore/?sort=modified
# - https://documentation-resources.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/table/?disjunctive.cou_name_en
# - https://documentation-resources.opendatasoft.com/explore/dataset/doc-geonames-cities-5000/table/
# - https://documentation-resources.opendatasoft.com/explore/dataset/us-cities-demographics/table/
# - https://documentation-resources.opendatasoft.com/explore/dataset/natural-earth-countries-110m/table/

# Get samples of the vehicle model data
curl -v "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?limit=100" > vehicles.txt
cat vehicles.txt | jq > vehicles.json

# Get the lists of car Makers 
curl -v "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?group_by=make&order_by=make&limit=100&offset=0" > makes1.txt
curl -v "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?group_by=make&order_by=make&limit=100&offset=100" > makes2.txt
cat makes1.txt | jq > makes1.json
cat makes2.txt | jq > makes2.json

# Subaru
curl -v "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?select=make%2C%20model%2C%20city08u%2C%20highway08u%2C%20comb08u%2C%20cylinders%2C%20displ%2C%20drive%2C%20eng_dscr%2C%20fueltype1%2C%20id%2C%20trany%2C%20vclass%2C%20year%2C%20mfrcode%2C%20basemodel&where=make%20%3D%20%22Subaru%22&order_by=make%2C%20model%2C%20year&limit=100&offset=0" > subaru1.txt
cat subaru1.txt | jq > subaru1.json

# Tesla
curl -v "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?select=make%2C%20model%2C%20city08u%2C%20highway08u%2C%20comb08u%2C%20cylinders%2C%20displ%2C%20drive%2C%20eng_dscr%2C%20fueltype1%2C%20id%2C%20trany%2C%20vclass%2C%20year%2C%20mfrcode%2C%20basemodel&where=make%20%3D%20%22Tesla%22&order_by=make%2C%20model%2C%20year&limit=100&offset=0" > tesla1.txt
cat tesla1.txt | jq > tesla1.json
