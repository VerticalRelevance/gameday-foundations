import boto3
import logging
import zipfile
from pathlib import Path
def handler(event, context):

    ssm = boto3.client('ssm')
    codepipeline = boto3.client('codepipeline')
    s3 = boto3.client('s3')

    job_data = event['CodePipeline.job']['data']
    bucket_name = job_data['inputArtifacts']['location']['s3Location']['bucket_name']
    object_key = job_data['inputArtifacts']['location']['s3Location']['bucket_name']
    credentials = job_data['artifact_credentials']

    s3.download_file(bucket_name, object_key, '/tmp/artifact.zip')

    try:
        with zipfile.ZipFile('/tmp/artiact.zip') as zip:
            zip.extractall('/tmp/documents')
        directory = "TODO FIGURE OUT HOW TO GET SOURCE OUTPUT"

        files = Path(directory).glob('*')
        ssm = boto3.client('ssm')
        for doc in files:
            name = Path(doc).stem
            with open(doc) as f:
                content : f.read()
                ssm.create_document(
                    Content='content',
                    Name = name,
                    DocumentType = 'Automation'            
                )
    except Exception as er:

        print(er)
        codepipeline.put_job_failure_reslt(
            jobId=event['CodePipeline.job']['id'], 
            failureDetails={'message': str(er), 'type': 'JobFailed'})







    