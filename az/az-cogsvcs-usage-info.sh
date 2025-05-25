#!/bin/bash

# Capture info about your Azure Cognitive Services account usage.
#
# Chris Joakim, 2025

echo "az cognitiveservices usage list ..."
az cognitiveservices usage list \
    --location $AZURE_FOUNDRY_REGION > ../datasets/azure/usage-list.json
