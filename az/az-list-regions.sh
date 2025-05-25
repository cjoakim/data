#!/bin/bash

# List the Azure regions available to your subscription.
#
# Chris Joakim, 2025

echo "az account list-locations names ..."
az account list-locations --query "[].{Region:name}" --out table > ../datasets/azure/region-names.txt 

echo "az account list-locations datails ..."
az account list-locations --out json > ../datasets/azure/region-details.json 
