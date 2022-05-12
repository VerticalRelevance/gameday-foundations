#!/bin/bash

npm install -g aws-cdk
cd runbooks
echo "Entered Runbooks directory"

for file in *.yml; do
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
        --document-version '$LATEST' \
        && aws ssm update-document-default-version \
            --name "$docname" \
            --document-version '$LATEST'
done 