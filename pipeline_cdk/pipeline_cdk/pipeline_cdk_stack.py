from aws_cdk import (
    # Duration,
    Stack,
    pipelines as pipelines,
    aws_codepipeline as codepipeline,
    aws_codestarconnections as codestar,
    aws_codebuild as codebuild,
    aws_codepipeline_actions as codepipeline_actions,
    aws_ssm as ssm,
    aws_iam as iam
)

from cdk_ssm_document import Document
import os
from pathlib import Path
from constructs import Construct
import aws_cdk as core
import boto3


class GameDayPipelineStack(Stack):

   
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        #codestar_connections_github_arn = core.SecretValue.secrets_manager("gameday-foundations-pipeline-secret").to_string()

        client = boto3.client("secretsmanager", "us-east-1")
        codestar_connections_github_arn = client.get_secret_value(
            SecretId='gameday-foundations-pipeline-secret')["SecretString"].rstrip()
        #github_token = client.get_secret_value(
        #     SecretId='gameday-pipeline-github-token')["SecretString"].rstrip()

        #source_output = codepipeline.Artifact()
        pipeline = pipelines.CodePipeline(
            self, "GameDayPipeline",
            self_mutation=False,
            synth=pipelines.ShellStep("Synth",
                                      input=pipelines.CodePipelineSource.git_hub(
                                          "VerticalRelevance/gameday-foundations",
                                          "dev",
                                          authentication=core.SecretValue.secrets_manager(
                                              'gameday-pipeline-github-token'
                                          )
                                      ),
                                        commands= ["chmod u+x upload.sh", "./upload.sh"],
                                        #primary_output_directory="pipeline_cdk/cdk.out"

                                        
            ),
            code_build_defaults=pipelines.CodeBuildOptions(

                role_policy=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "ssm:CreateDocument",
                            "ssm:UpdateDocument"
                        ],

                        resources=[
                            "*"
                        ]
                    )
                ]    
            ),

            synth_code_build_defaults=pipelines.CodeBuildOptions()
        )
