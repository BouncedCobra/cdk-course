#!/usr/bin/env python3
import os

import aws_cdk as cdk

from py_starter.py_starter_stack import PyStarterStack


app = cdk.App()
PyStarterStack(app, "PyStarterStack",
               env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))

app.synth()
