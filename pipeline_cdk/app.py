#!/usr/bin/env python3
import os

import aws_cdk as cdk
from pipeline_cdk.pipeline_cdk.pipeline_cdk_stack import GameDayPipelineStack

from pipeline_cdk.pipeline_cdk_stack import GameDayPipelineStack


app = cdk.App()
GameDayPipelineStack(app, "gameday-foundation-pipeline")

app.synth()
