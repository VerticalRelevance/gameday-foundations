from xml.dom.minidom import DocumentType
import boto3
import os
from pathlib import Path

directory = "TODO FIGURE OUT HOW TO GET SOURCE OUTPUT"

files = Path(directory).glob('*')
ssm = boto3.client('ssm')
for doc in files:
    name = os.path.basename(doc)
    with open(doc) as f:
        content : f.read()
        ssm.create_document(
            Content='content',
            Name = name,
            DocumentType = 'Automation'            
        )


    