from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    RemovalPolicy
)
from constructs import Construct

class PyStarterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the DynamoDB table
        table = dynamodb.Table(
            self, "MyTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY #what does this do?, it deletes the table when the stack is deleted
        )

        # Define the Lambda function
        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='lambda_function.handler',
            code=_lambda.Code.from_asset('resources/lambdas/lambda_function')
        )

        # Define the IAM policy for DynamoDB access
        dynamo_policy = iam.PolicyStatement(
            actions=[
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem",
                "dynamodb:Scan",
                "dynamodb:Query"
            ],
            resources=[table.table_arn]
        )

        # Attach the policy to the Lambda function's role
        lambda_function.add_to_role_policy(dynamo_policy)

        # Define the API Gateway REST API
        api = apigateway.RestApi(
            self, 'MyApiGateway',
            rest_api_name='My Service',
            description='This service serves my Lambda function.'
        )

        # Create a Lambda integration
        lambda_integration = apigateway.LambdaIntegration(
            lambda_function,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        # Add a method to the API Gateway resource
        api.root.add_method('GET', lambda_integration)