#!/bin/bash

npm install -g aws-cdk
cd runbooks
echo "Entered Runbooks directory"

for file in *.yml; do
    echo "Attempting to upload new SSM Automation Document: $file"
    docname=$(basename "$file" .yml)
    aws ssm create-document \
        --content file://"$file" \
        --name "$docname" \
        --document-format "YAML" \
        --document-type "Automation" \
    || 
    echo "Attempting to update existing SSM Automation Document: $file"
    aws ssm update-document \
        --content file://"$file" \
        --name "$docname" \
        --document-format "YAML" \
        --document-version '$LATEST'
    version=$(aws ssm list-document-versions \
        --name "$docname" | jq '.DocumentVersions | .[0] | .DocumentVersion | tonumber') 
    aws ssm update-document-default-version \
    --name "$docname" \
    --document-version "$version"
done 