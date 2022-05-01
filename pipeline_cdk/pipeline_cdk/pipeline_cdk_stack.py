from aws_cdk import (
    # Duration,
    Stack,
    pipelines as pipelines,
    aws_codepipeline as codepipeline,
    aws_codestarconnections as codestar,
    aws_codebuild as codebuild,
    aws_codepipeline_actions as codepipeline_actions,
)
from constructs import Construct

class PipelineCdkStack(Stack):

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
        pipeline = pipelines.Pipeline(
            self, "Pipeline", 
            pipeline_name="Gameday-Pipeline",

            stages=[
                codepipeline.StageProps(stage_name="Source", actions = [source_action]),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions = [ 
                        codepipeline_actions.CodeBuildAction(
                        action_name="Build",
                        project=codebuild.PipelineProject(self, "MyProject"),
                        input=source_output
                        )
                    ],
                )
               
            ]
            
            

             
            

        )
            


      
       

