#!/bin/bash

# Execute the several data-capturing scripts in this directory.
#
# Chris Joakim, 2025

./az-list-regions.sh
./az-cogsvcs-model-list.sh
./az-cogsvcs-usage-info.sh

echo "done"
