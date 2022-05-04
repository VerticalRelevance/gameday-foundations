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

class PipelineCdkStack(Stack):
 
    def createCodePipelinePolicy(self, codestar_connections_github_arn):
        codepipeline_policy= iam.ManagedPolicy(
            self, "codepipeline_policy",
            managed_policy_name="codepipeline_policy_gameday",
            statements=[
                iam.PolicyStatement(
                    effect = iam.Effect.ALLOW,
                    actions= [
                        "ssm:CreateDocument"
                    ],

                    resources=[
                        "document"
                    ]
                ),

                iam.PolicyStatement(
                    effect = iam.Effect.ALLOW,
                    actions= [
                        "codestar-connections:UseConnection"
                    ],
                    resources=[
                        codestar_connections_github_arn
                    ],
                ),

                iam.PolicyStatement(
                    effect = iam.Effect.ALLOW,
                    actions = [
                        "codebuild:StartBuild"
                    ],

                )
            ]
        )

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        codestar_connections_github_arn = "arn:aws:codestar-connections:region:account-id:connection/connection-id"

        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
                action_name="Github",
                owner="VerticalRelevance",
                repo="gameday-foundations",
                output=source_output,
                connection_arn= codestar_connections_github_arn,
            ),
        pipeline = pipelines.CodePipeline(
            self, "Pipeline", 
            self_mutation=False,
            synth = pipelines.ShellStep("Synth",
                input = pipelines.CodePipelineSource.connection(
                    "VerticalRelevance/gameday-foundations",
                    "dev",
                    connection_arn = "arn:aws:codestar-connections:region:account-id:connection/connection-id"
                ),

            
            commands = ["./upload.sh"]
            )
        )

            #What to do here? How do I link this build action with
            ##the uplopad? Should I use a Lambda?
       
            


      
       

