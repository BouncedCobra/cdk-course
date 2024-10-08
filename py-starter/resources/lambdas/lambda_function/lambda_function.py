import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')

def handler(event, context):

    # Scan the DynamoDB table
    response = table.scan()
    items = response['Items']
    print(items)
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }