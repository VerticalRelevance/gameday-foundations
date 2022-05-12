import boto3
import logging
import zipfile
from pathlib import Path
def handler(event, context):

    ssm = boto3.client('ssm')
    """
    Runs SSM Automation Document (Runbook) by the input:

    'runbook_name': "ec2_runbook.yml",
    'automation_assume_role': "iamRole"
    
    """
    runbook = event.get('runbook_name')
    assumed_role = event.get('automation_assume_role')
    ssm.start_automation_execution(DocumentName = runbook,
        Parameters={
            'AutomationAssumeRole': [
                assumed_role
            ]
        }
    )



    