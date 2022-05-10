import aws_cdk as core
import aws_cdk.assertions as assertions

from gameday_lambda.gameday_lambda_stack import GamedayLambdaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in gameday_lambda/gameday_lambda_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GamedayLambdaStack(app, "gameday-lambda")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
