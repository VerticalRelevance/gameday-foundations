#!/bin/bash

npm install -g aws-cdk
cd runbooks
echo "Entered Runbooks directory"

for file in *; do
    echo "uploading $file"
    docname=$(basename "$file" .yml)
    aws ssm create-document \
        --content file://"$file" \
        --name "$docname" \
        --document-format "YAML" \
        --document-type "Automation" \
    || aws ssm update-document \
        --content file://"$file" \
        --name "$docname" \
        --document-format "YAML" \
        --document-type "Automation"
done 