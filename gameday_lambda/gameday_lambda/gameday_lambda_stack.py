import os
import random
import zipfile
from aws_cdk import (
    Duration,
    aws_kms as kms,
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as lambda_,
    Stack,
    aws_s3_deployment as s3deploy
    
    # aws_sqs as sqs,
)
import aws_cdk as core
from constructs import Construct

class GamedayLambdaStack(Stack):
    def createIAMRole(self, name, service_principal_list):
        composite_principal = iam.CompositePrincipal(
            iam.ServicePrincipal(service_principal_list[0])
        )
        if len(service_principal_list) > 1:
            for service_principal in service_principal_list[1:]:
                composite_principal.add_principals(
                    iam.ServicePrincipal(service_principal)
                )
        role = iam.Role(
            self, name, assumed_by=composite_principal, path=None, role_name=name
        )
        return role
    def createKMSKey(self, name, description):
        key = kms.Key(
            self,
            name,
            description=description,
            pending_window=core.Duration.days(14),
            enable_key_rotation=True,
        )
        return key
    def createGamedayLambdaIAMPolicy(self):
        gameday_lambda_policy = iam.ManagedPolicy(
            self,
            "gameday_lambda_policy",
            managed_policy_name="gameday_lambda_policy",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["ssm:StartAutomationExecution"],
                    resources = ["*"]
                ),
                 iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["ec2:DescribeInstances"],
                    resources=["*"],
                ),
                
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "ec2:RunInstances",
                        "ec2:TerminateInstances",
                        "ec2:StopInstances",
                        "ec2:StartInstances",
                    ],
                    resources=["*"],
                ),
            ],

        )
        return gameday_lambda_policy

    def uploadLambdaCode(self, random_bucket_suffix):
        

        def zipdir(path, ziph):
            length = len(path)

            for root, dirs, files in os.walk(path):
                directory = root[length:]
                for file in files:
                    ziph.write(os.path.join(root, file), os.path.join(directory, file))

        with zipfile.ZipFile("gameday_code.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
            zipdir("../lambda/", zipf)

        zipfile.ZipFile("gameday_code_zipped.zip", mode="w").write("gameday_code.zip")

        lambda_code_bucket = s3.Bucket(
            self,
            "gameday_code_bucket" + random_bucket_suffix,
            bucket_name="resiliency-lambda-code-bucket" + random_bucket_suffix,
            access_control=s3.BucketAccessControl.PRIVATE,
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        code_upload = s3deploy.BucketDeployment(
            self,
            "LambdaCodeSource",
            sources=[s3deploy.Source.asset("gameday_code_zipped.zip")],
            destination_bucket=lambda_code_bucket,
        )

        return {"lambda_code_bucket": lambda_code_bucket, "code_upload": code_upload}

    def createFunction(self, gameday_lambda_role, gameday_code_bucket, code_upload):
        lambda_function = lambda_.Function(
            self,
            "lambda_function",
            function_name = "GamedayLambdaFunction",
            role = gameday_lambda_role,
            runtime = lambda_.Runtime.PYTHON_3_9,
            handler = "handler.handler",
            code = lambda_.Code.from_bucket(
                bucket = gameday_code_bucket, key="gameday_code.zip"
            ),
            memory_size = 1024,
            timeout = Duration.seconds(800)
        )

        lambda_function.node.add_dependency(code_upload)

        return lambda_function

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        random_bucket_suffix = str(random.randint(100000, 999999))

        s3_key = GamedayLambdaStack.createKMSKey(
            self, "s3_key", "Encrypt s3 resources"
        )

        gameday_lambda_role = GamedayLambdaStack.createIAMRole(
            self, "gameday_lambda_role", ["lambda.amazonaws.com"]
        )

        gameday_lambda_policy = GamedayLambdaStack.createGamedayLambdaIAMPolicy(self)

        gameday_lambda_policy.attach_to_role(gameday_lambda_role)

        code_upload_resources = GamedayLambdaStack.uploadLambdaCode(
            self, random_bucket_suffix
        )

        code_upload = code_upload_resources["code_upload"]
        lambda_code_bucket = code_upload_resources["lambda_code_bucket"]

        lambda_function = GamedayLambdaStack.createFunction(
            self, gameday_lambda_role, lambda_code_bucket, code_upload
        )

