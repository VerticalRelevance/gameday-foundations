#!/bin/bash

npm install -g aws-cdk
cd runbooks
echo "Entered Runbooks directory"

for file in "/runbooks"/*; do
    echo "uploading $file"
    docname = basename $file .yml
    aws ssm create-document \
        --content file://$file
        --name $docname
        --document-type "Automation"